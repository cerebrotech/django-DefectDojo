import csv,json


def get_existing_containers_list(existing_ownership_file):
    existing_containers_to_owners_dict={}
    with open(existing_ownership_file) as fp:
        csv_reader=csv.reader(fp)
        for i,row in enumerate(csv_reader):
            if i==0:
                print("header row")
                # print(row)
            else:
                container_name=row[0]
                container_tag=row[1]
                owner=row[2]
                existing_containers_to_owners_dict[container_name]=owner

    return existing_containers_to_owners_dict

if __name__ == '__main__':
    eng_ownership_file_path='/Users/mannysingh/Documents/daily-work/eng_ownership/master_container_ownership .csv'
    existing_containers_to_owners_dict=get_existing_containers_list(eng_ownership_file_path)
