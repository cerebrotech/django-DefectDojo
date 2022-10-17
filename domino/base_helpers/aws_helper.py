import  boto3
import base64
from botocore.exceptions import ClientError
import json
from pprint import pprint
import time


class AwsResponseChecker(object):
    def __init__(self,aws_response):
        self.aws_response=aws_response

    @property
    def response_metadata(self):
        return self.aws_response.get('ResponseMetadata')

    @property
    def http_headers(self):
        return self.response_metadata.get('HTTPHeaders')

    @property
    def status_code(self):
        return self.response_metadata.get('HTTPStatusCode')



class AwsApi(object):
    # def __init__(self, awsEndpoint,*args,assume_profile=None):
    def __init__(self, awsEndpoint,**kwargs):
        '''
        :param awsEndpoint: aws endpoint eg iam, s3
        :param kwargs assume_profile: assume_profile=profile_name
        :param kwargs assume_role: assume_role=role_arn to assume via assume_profile or default profile
        :param kwargs assume_role: region=region_name
        '''
        self.session = None
        self.kwargs=kwargs
        self.awsEndpoint = awsEndpoint
        # self.args=args
        self.assume_role = self._return_variable('assume_role')
        self.region = self._return_variable('region')
        self.profile = self._return_variable('profile')


    def _return_variable(self,variable):
        if variable in self.kwargs.keys():
            return self.kwargs[variable]
        else:
            return None


    @property
    def get_aws_session(self):
        if self.assume_role is None:
            if self.region and  self.profile:
                self.session = boto3.session.Session(region_name=self.region, profile_name=self.profile)
            elif  self.region and self.profile==None:
                self.session = boto3.session.Session(region_name=self.region)
            elif self.region==None and self.profile:
                self.session = boto3.session.Session(profile_name=self.profile)
            elif self.region==None and self.profile==None:
                self.session = boto3.session.Session()
            else:
                print("Passed more than 2 arguments: {}".format(self.args))
                exit(11)
        else:
            #here we need to assume role either via default profile or mentioned profile
            session_name = self.assume_role.split("/")[-1]

            if self.profile:
                _temp_session = boto3.session.Session( profile_name=self.profile)
            else:
                _temp_session = boto3.session.Session()
            response = _temp_session.client('sts').assume_role(RoleArn=self.assume_role, RoleSessionName=session_name)
            if self.region:
                self.session = boto3.session.Session(region_name=self.region,
                                                     aws_access_key_id=response['Credentials']['AccessKeyId'],
                                                     aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                                                     aws_session_token=response['Credentials']['SessionToken'])
            else:
                self.session = boto3.session.Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                                                     aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                                                     aws_session_token=response['Credentials']['SessionToken'])
        return self.session

    @property
    def get_boto3_client(self):
        return self.get_aws_session.client(self.awsEndpoint)

    @property
    def get_boto3_resource(self):
        return self.get_aws_session.resource(self.awsEndpoint)




class SecrertsManagerOperations(AwsApi):

    def __init__(self,**kargs):
        self.awsEndpoint = 'secretsmanager'
        AwsApi.__init__(self, self.awsEndpoint, **kargs)
        return

    def get_secret(self,secret_name):
        # secret_name = "whitesource-automation/api-keys"

        try:
            get_secret_value_response = self.get_boto3_client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            else:
                print(e)
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return json.loads(secret)


class S3Operations(AwsApi):
    def __init__(self,**kwargs):
        self.awsEndpoint='s3'
        AwsApi.__init__(self, self.awsEndpoint,**kwargs)
        return

    def getS3Object(self, objectName, bucketName):
        return self.get_boto3_resource.Bucket(bucketName).Object(objectName).get()['Body'].read()

    def putS3Object(self, objectName, objectBody, bucketName, contentType):
        return self.get_boto3_resource.Bucket(bucketName).Object(objectName).put(Body=objectBody,
                                                                                        ContentType=contentType)
    def upload_file(self,path_to_file, bucket_to_upload, file_name):
        return  self.get_boto3_resource.meta.client.upload_file(path_to_file, bucket_to_upload, file_name)

    def check_if_object_exists(self,object_path,s3_bucket):
        try:
            self.get_boto3_resource.Object(s3_bucket, object_path).load()
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                # The object does not exist.
                return False
            else:
                # Something else has gone wrong.
                raise
        else:
            return True


    def listDirectoriresFromS3(self, location, bucket):
        dirList = []
        response = self.get_boto3_client.list_objects_v2(Bucket=bucket, Prefix=location, Delimiter="/")
        for item in response['CommonPrefixes']:
            if item['Prefix'] != "index.html":
                dirList.append(item['Prefix'])
        return dirList

    def listFilesFromS3(self, location, bucket):
        fileList = []
        response = self.get_boto3_client.list_objects_v2(Bucket=bucket, Prefix=location, Delimiter="/")
        try:
            if len(response['Contents']) >0:
                for item in response['Contents']:
                    if location[1:] in item['Key'] and location != item['Key']:
                        fileList.append(item['Key'])
            return fileList
        except Exception as e:
            print("Got exception,")
            print(location, bucket)
            raise e



    def list_files_and_folders_S3(self,location, bucket):
        response = self.get_boto3_client.list_objects_v2(Bucket=bucket, Prefix=location, Delimiter="/")
        final_list=[]
        if "Contents" in response.keys():
            for item in response['Contents']:
                if location[1:] in item['Key'] and location != item['Key'] and "index.html" not in item['Key']:
                    final_list.append(item['Key'])
        if "CommonPrefixes" in response.keys():
            for item in response['CommonPrefixes']:
                if item['Prefix'] != "index.html":
                    final_list.append(item['Prefix'])
        if "/" in final_list:
            final_list.remove("/")
        return final_list


class PrivateCa(AwsApi):
    def __init__(self,**kwargs):
        self.awsEndpoint='acm-pca'
        AwsApi.__init__(self, self.awsEndpoint,**kwargs)

    def revoke_crt(self,serial,ca_arn):
        response = self.get_boto3_client.revoke_certificate(
            CertificateAuthorityArn=ca_arn,
            CertificateSerial=serial,
            RevocationReason='CESSATION_OF_OPERATION'
        )

    def get_pca_cert(self,cert_arn):
        _authority_arn=cert_arn.split("/certificate")[0]
        response = self.get_boto3_client.get_certificate(CertificateAuthorityArn=_authority_arn,CertificateArn=cert_arn)
        return response['Certificate']

class Acm(AwsApi):
    def __init__(self,**kwargs):
        self.awsEndpoint='acm'
        AwsApi.__init__(self,self.awsEndpoint,**kwargs)


    def paginated_list_certs_issued(self):
        certs_dict_arns={}
        paginator=self.get_boto3_client.get_paginator('list_certificates')
        response_iterator = paginator.paginate(
            CertificateStatuses=['ISSUED'],
        )
        for page in response_iterator:
            certs_list=page['CertificateSummaryList']
            for cert in certs_list:
                certs_dict_arns[cert['CertificateArn']]=cert['DomainName']
        return certs_dict_arns

    def paginated_list_certs_all(self):
        certs_dict_arns={}
        paginator=self.get_boto3_client.get_paginator('list_certificates')
        response_iterator = paginator.paginate(
            # CertificateStatuses=['ISSUED'],
        )
        for page in response_iterator:
            certs_list=page['CertificateSummaryList']
            for cert in certs_list:
                certs_dict_arns[cert['CertificateArn']]=cert['DomainName']

        return certs_dict_arns

    def get_cert(self,arn):
        response = self.get_boto3_client.get_certificate(
            CertificateArn=arn
        )
        return response

    def describe_cert(self,arn):
        response = self.get_boto3_client.describe_certificate(CertificateArn=arn)
        return response['Certificate']


    def uploade_new_cert(self,crt_bytes,key_bytes,chain_bytes,service,jira):
        response=self.get_boto3_client.import_certificate(
            Certificate=crt_bytes,
            PrivateKey=key_bytes,
            CertificateChain=chain_bytes,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': service
                },
                {
                    'Key': 'jira-{}'.format(time.strftime('%Y-%m-%d-%l_%M%p%z')),
                    'Value': jira
                }
            ])
        return response


class Elb(AwsApi):
    def __init__(self,**kwargs):
        self.awsEndpoint='elb'
        AwsApi.__init__(self, self.awsEndpoint,**kwargs)

    def describe_lb(self,pageSize=400,elbs_list=[],marker=None):
        if marker is None:
            elbs_list.clear()
            response=self.get_boto3_client.describe_load_balancers(PageSize=pageSize)
        else:
            response = self.get_boto3_client.describe_load_balancers(PageSize=pageSize,Marker=marker)
        elbs_list +=response['LoadBalancerDescriptions']
        if 'NextMarker' in response.keys():
            self.describe_lb(pageSize=pageSize,marker=response['NextMarker'],elbs_list=elbs_list)
        return elbs_list

    def describe_tag(self,elb_names_list):
        response = self.get_boto3_client.describe_tags(LoadBalancerNames=elb_names_list)
        return response['TagDescriptions']



class Elbv2(AwsApi):
    def __init__(self,**kwargs):
        self.awsEndpoint='elbv2'
        AwsApi.__init__(self, self.awsEndpoint,**kwargs)

    def describe_lb(self,pageSize=400,elbs_list=[],marker=None):
        if marker is None:
            elbs_list.clear()
            response=self.get_boto3_client.describe_load_balancers(PageSize=pageSize)
        else:
            response = self.get_boto3_client.describe_load_balancers(PageSize=pageSize,Marker=marker)
        elbs_list +=response['LoadBalancers']
        if 'NextMarker' in response.keys():
            self.describe_lb(pageSize=pageSize,marker=response['NextMarker'],elbs_list=elbs_list)
        return elbs_list

    def describe_listner(self,elbv2_arn,listeners_list=[],pageSize=100,marker=None):
        if marker is None:
            listeners_list.clear()
            response = self.get_boto3_client.describe_listeners(LoadBalancerArn=elbv2_arn,PageSize=pageSize)
        else:
            response = self.get_boto3_client.describe_listeners(LoadBalancerArn=elbv2_arn, Marker=marker,PageSize=pageSize)
        listeners_list += response['Listeners']
        if 'NextMarker' in response.keys():
            self.describe_listner(self,elbv2_arn,listeners_list=listeners_list,pageSize=pageSize,marker=response['NextMarker'])
        return listeners_list

    def describe_tagv2(self,elb_arns_list):
        response = self.get_boto3_client.describe_tags(ResourceArns=elb_arns_list)
        return response


class Iam(AwsApi):
    def __init__(self,**kwargs):
        self.awsEndpoint = 'iam'
        AwsApi.__init__(self, self.awsEndpoint, **kwargs)

    def list_certificates(self,certs_list=[],marker=None,maxItems=100):
        if marker is None:
            certs_list.clear()
            response=self.get_boto3_client.list_server_certificates(MaxItems=maxItems)
        else:
            response = self.get_boto3_client.list_server_certificates( Marker=marker, MaxItems=maxItems)
        certs_list += response['ServerCertificateMetadataList']
        if 'Marker' in response.keys():
            self.list_certificates(certs_list=certs_list,marker=response['Marker'], maxItems=maxItems)
        return certs_list

    def download_cert(self,cert_name):
        response = self.get_boto3_client.get_server_certificate(ServerCertificateName=cert_name)
        return response['ServerCertificate']['CertificateBody']

class CloudFront(AwsApi):
    def __init__(self,**kwargs):
        self.awsEndpoint = 'cloudfront'
        AwsApi.__init__(self, self.awsEndpoint, **kwargs)

    def list_distros(self,distros_list=[],marker=None,maxItems=100):
        maxItems=str(maxItems)
        if marker is None:
            distros_list.clear()
            response = self.get_boto3_client.list_distributions(MaxItems=maxItems)
        else:
            response = self.get_boto3_client.list_distributions( Marker=marker, MaxItems=maxItems)
        distros_list += response['DistributionList']['Items']

        if 'NextMarker' in response['DistributionList'].keys():
            next_marker=response['DistributionList']['NextMarker']
            self.list_distros(distros_list=distros_list,marker=next_marker,maxItems=maxItems)
        return distros_list

class Sts(AwsApi):
    def __init__(self,**kwargs):
        endpoint='sts'
        AwsApi.__init__(self,endpoint,**kwargs)

    @property
    def account_id(self):
        return self.get_boto3_client.get_caller_identity()['Account']



class Ec2(AwsApi):
    def __init__(self,**kwargs):
        _awsEndpoint='ec2'
        AwsApi.__init__(self,_awsEndpoint,**kwargs)


    def describe_active_instances(self,instances_list=[],marker=None,maxItems=1000):
        if marker is None:
            instances_list.clear()
            response=self.get_boto3_client.describe_instances(Filters=[{'Name': 'instance-state-name','Values': ['running']}],
                                                              MaxResults=maxItems)
        else:
            response = self.get_boto3_client.describe_instances(Filters=[{'Name': 'instance-state-name','Values': ['running']}],
                                                                MaxResults=maxItems,NextToken=marker)

        instances_list +=[instance[0] for instance in [instances['Instances'] for instances in response['Reservations']]]
        # print(len(response['Reservations']))
        if 'NextToken' in response.keys():
            marker=response['NextToken']
            self.describe_active_instances(maxItems=maxItems,marker=marker)
        # print(len(instances_list))
        return instances_list

    def decribe_security_grps(self,groups_list=[],marker=None,maxItems=1000):
        if marker is None:
            groups_list.clear()
            response=self.get_boto3_client.describe_security_groups(MaxResults=maxItems)
        else:
            response = self.get_boto3_client.describe_security_groups(MaxResults=maxItems,NextToken=marker)

        groups_list += response['SecurityGroups']
        if 'NextToken' in response.keys():
            marker=response['NextToken']
            self.decribe_security_grps(maxItems=maxItems,marker=marker)
        return groups_list


class StepFunctions(AwsApi):
    def __init__(self,**kwargs):
        _awsEndpoint='stepfunctions'
        AwsApi.__init__(self,_awsEndpoint,**kwargs)


    def _convert_dict_to_escaped_json(self,dict_input):
        _input=str(json.dumps(dict_input).replace('"','\\"'))
        return _input

    def start_step_machine(self,machine_arn,execution_name,dict_input):
        # print('"{}"'.format(self._convert_dict_to_escaped_json(dict_input)))
        response=self.get_boto3_client.start_execution(
            stateMachineArn=machine_arn,
            name=execution_name,
            input=json.dumps(dict_input)
        )

        response_obj=AwsResponseChecker(response)

        return response_obj.status_code








if __name__ == '__main__':
    # acm_obj=Acm('us-west-2','dev')
    # issued_list=acm_obj.paginated_list_certs_issued()
    # arns_list=issued_list.keys()
    # for arn in arns_list:
    #     describe_cert_response=acm_obj.describe_cert(arn)
    #     try:
    #         serial=describe_cert_response['Serial'].replace(":","")
    #         in_use_by=describe_cert_response['InUseBy']
    #         print(serial,in_use_by)
    #     except:
    #         pprint.pprint(describe_cert_response)
    #         exit(11)
        # print(json.dumps(describe_cert_response,indent=1))

    # elb_obj=Elbv2(profile='dev',region='us-west-2')
    # pprint(elb_obj.describe_lb(pageSize=1))
    region='us-west-2'
    profile='dev'
    # iam_obj = Iam(region=region, profile=profile)
    #     # print(iam_obj.download_cert('wild.protect.staging.lkt.is_AISEC-1481'))

    # cdn_obj=CloudFront(region=region,profile=profile)
    # pprint(cdn_obj.list_distros())

    ec2_obj=Ec2(profile=profile,region=region)
    # pprint(ec2_obj.decribe_security_grps())
    # instances_list=ec2_obj.describe_active_instances()
    # for instance in instances_list:
    #     try:
    #         print(instance['Tags'])
    #     except:
    #         pprint(instance)
    #         exit(11)

    # sts_obj=Sts(profile=profile,region=region)
    # print(sts_obj.account_id)

    # s=S3Operations(region='us-west-2')
    # print(s.list_files_and_folders_S3('','infosec-testing-ddl'))

    m_arn='arn:aws:states:us-west-2:482871598378:stateMachine:HelloWorld'
    d={'1':'1'}
    sfn_obj=StepFunctions()
    status_code=(sfn_obj.start_step_machine(m_arn,'hello1234',d))
    print(status_code)