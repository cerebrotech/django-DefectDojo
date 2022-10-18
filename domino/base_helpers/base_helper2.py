import csv
import json
import requests
import time
from os import listdir
from  os.path import exists
from  os.path import dirname
from os import makedirs
from os.path import isdir,join
from os import _exit
from os import getcwd
from os import environ
import errno
from multiprocessing.pool import ThreadPool
import traceback
from shutil import rmtree
from datetime import datetime,timedelta
import subprocess
import shutil
from os.path import expanduser


def iter_dict_into_properties(j, initial="input_json"):
    for k, v in j.items():
        if initial != 'input_json':
        # if initial:
            function_name = initial + '_' + k
        else:
            function_name = k
        function = '''
    @property
    def {}(self):
        return self.{}['{}']'''.format(function_name, initial, k)

        print(function)

        if isinstance(v, dict):
            iter_dict_into_properties(v, initial=function_name)


def delete_folder_rmtree(folder):
    shutil.rmtree(folder)


def get_home(dir=''):
    return expanduser("~/{}".format(dir))


def move_files_and_folders(source_folder_with_slash, destination_folder_with_slash):
    file_names = listdir(source_folder_with_slash)
    for file_name in file_names:
        shutil.move(join(source_folder_with_slash, file_name), destination_folder_with_slash)

def delete_folder_rmtree(folder):
    shutil.rmtree(folder)

def get_time_now():
    return str(datetime.now()).replace(" ","-").replace(":","-")

def todays_date():
    return datetime.now().strftime('%Y/%m/%d/')

def todays_date_dash():
    return datetime.now().strftime('%Y-%m-%d')

def yesterdays_date():
    yesterday = datetime.now() - timedelta(1)
    return datetime.strftime(yesterday, '%Y/%m/%d/')

def running_locally():
    pwd=getcwd()
    if 'manny' in pwd.lower():
        return True
    else:
        return False


def run_command(command,working_dir=False,command_msg=' ',env=None,capture_output=False):

    if env==None:
        env=dict(os.environ)
    # return subprocess.getoutput(command)
    try:
        # output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        if working_dir:
            output = subprocess.run(command, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True,
                                    cwd=working_dir, shell=True,env=dict(env),executable='/bin/bash')
        else:
            output = subprocess.run(command, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True,
                                    shell=True,env=env,executable='/bin/bash')
    except subprocess.CalledProcessError as exc:
        print(command_msg," Status : FAIL", exc.returncode, exc.output)
        print("Exiting....")
        exit(11)
    else:
        #check for return code here
        if int(output.returncode) !=0:
            print(command_msg,"Return code is non zero")
            print(command_msg,"Return code: ",output.returncode)
            print(command_msg,"command: ",output)
            print(command_msg,"Output: ",output.stdout)
            exit(11)
        else:
            print(command_msg," Command completed, return code: ",output.returncode)
            # print("Success: \n{}\n".format(output))
        return output


def delete_dir(dir_path):
    if exists(dir_path):
        rmtree(dir_path)


def make_csv(rows_list,file_location_to_save):
    with open(file_location_to_save,'w') as file_obj:
        csv_writer=csv.writer(file_obj)
        csv_writer.writerows(rows_list)

def save_file_with_data(data,file_location_to_save):
    with open(file_location_to_save,'w') as file_obj:
        file_obj.writelines(data)

def save_json(dict_to_save,file_location_to_save):

    with open(file_location_to_save,'w') as file_obj:
        json.dump(dict_to_save,file_obj,indent=1)

def jprint(data,ident=1):
    print(json.dumps(data,indent=ident))


def send_to_slack(json_data,webhookUrl):
    # webhookUrl = ''
    respose = requests.post(webhookUrl, json={"text": "{}".format(json_data)})

def response_checker(response,*args):
    if response.ok:
        return response.text
    else:
        print("Reponse has non ok code: ", response.text, *args)
        exit(11)


def dec_time(original_function):
    def wrapper_function(*args,**kwargs):
        print(original_function.__name__, "started")
        a_time = time.time()
        result= original_function(*args,**kwargs)
        b_time = time.time()
        time_taken = b_time - a_time
        print("{} completed in: {:.2f} seconds".format(original_function.__name__, time_taken))
        return  result
    return wrapper_function


def dec_time_return(original_function):
    def wrapper_function(*args,**kwargs):
        print(original_function.__name__, "started")
        a_time = time.time()
        result= original_function(*args,**kwargs)
        b_time = time.time()
        time_taken = b_time - a_time
        print("{} completed in: {:.2f} seconds".format(original_function.__name__, time_taken))
        return  time_taken,result
    return wrapper_function

def create_dir(filename):
    if not exists(dirname(filename)):
        try:
            makedirs(dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise



def list_files_recursive(reports_location,full_paths_list=[]):
    # print(reports_location)
    parent_list = listdir(reports_location)
    for location in parent_list:
        full_path=join(reports_location,location)
        if isdir(full_path):
            list_files_recursive(full_path,full_paths_list)
        else:
            # print("we need to upload:",full_path)
            if ".DS_Store" not in full_path:
                full_paths_list.append(full_path)
    return full_paths_list

def upload_files_to_s3(parent_location,files_to_upload_local_path,s3_parent_folder,bucket_name,s3_obj):
    s3_paths_list=[]
    for file in files_to_upload_local_path:
        s3_path_to_upload=file.replace(parent_location,s3_parent_folder)
        s3_paths_list.append(s3_path_to_upload)
        file_obj = open(file)
        s3_obj.putS3Object(s3_path_to_upload, file_obj.read(), bucket_name, 'text/csv')
        file_obj.close()
    return s3_paths_list

def error_handler_pool(e):
    print('error_callback()', e)
    traceback.print_exception(type(e), e, e.__traceback__)
    # exit(11)
    #todo, exit here
    _exit(12)

def upload_to_s3_singular(file,s3_path_to_upload,bucket_name, content_type,s3_obj):
    print("About to upload",file)
    file_obj = open(file)
    s3_obj.putS3Object(s3_path_to_upload, file_obj.read(), bucket_name, content_type)
    file_obj.close()



def upload_files_to_s3_threaded(parent_location,files_to_upload_local_path,s3_parent_folder,bucket_name,content_type,s3_obj,MAX_THREADS):
    s3_paths_list=[]
    pool = ThreadPool(processes=MAX_THREADS)
    while (files_to_upload_local_path):
        file=files_to_upload_local_path.pop()
        s3_path_to_upload=file.replace(parent_location,s3_parent_folder)
        s3_paths_list.append(s3_path_to_upload)
        pool.apply_async(upload_to_s3_singular,
                         (file,s3_path_to_upload,bucket_name, content_type,s3_obj),
                         error_callback=error_handler_pool)
    pool.close()  # Done adding tasks.
    pool.join()  # Wait for all tasks to complete.
    return s3_paths_list

def get_unique_locations_to_upload(s3_paths_list):
    unique_locations = []
    for file in s3_paths_list:
        # we don't care about actual filename
        unique_paths_in_file_name = file.split("/")[:-1]
        l = len(unique_paths_in_file_name) +1
        for i in range(1,l):
            path_joined='/'.join(unique_paths_in_file_name[0:i])
            unique_locations.append(path_joined)
    return list(set(unique_locations))

def createHtmlLinks(listOfLocations):
    linkList = []
    for item in listOfLocations:
        if "csv" in item or "zip" in item:
            linkTitle = item.split("/")[-1]
        else:
            linkTitle = item
        link = ('<a href="/{}">{}</a> <br /> \n'.format(item, linkTitle))
        linkList.append(link)
    return linkList

@dec_time
def create_and_upload_indexes(parent_location,s3_paths_list,bucket_name,s3_obj):
    unique_locations=get_unique_locations_to_upload(s3_paths_list)
    for index_location in unique_locations:
        #1. get list of files there
        files_at_index_location=s3_obj.list_files_and_folders_S3(index_location+"/",bucket_name)
        links_list=createHtmlLinks(files_at_index_location)
        local_path_for_index_file=parent_location +index_location +'/index.html'
        s3_path_for_index=index_location +'/index.html'
        print(s3_path_for_index,local_path_for_index_file)
        create_dir(local_path_for_index_file)
        with open(local_path_for_index_file,'w') as file_obj:
            for link in links_list:
                file_obj.writelines(link)
        index_body = open(local_path_for_index_file)
        s3_obj.putS3Object(s3_path_for_index, index_body.read(), bucket_name, 'text/html')
        index_body.close()


from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

def delete_create_dir(dir):
    if dir.endswith('/'):
        dir_with_slash=dir
        dir_without_slash="/".join((dir.split("/"))[:-1])
    else:
        dir_without_slash=dir
        dir_with_slash = dir +'/'

    delete_dir(dir_without_slash)
    create_dir(dir_with_slash)


if __name__ == '__main__':
    dir='/Users/manny/github/cerebrotech/container_scanning/sample_reports/local/'
    delete_create_dir(dir)