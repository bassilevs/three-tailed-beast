import boto3

from constants import BUCKET_NAME

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')


def create_directory(dir_name):
    directory_name = dir_name + "/"
    s3.put_object(Bucket=BUCKET_NAME, Key=(directory_name + '/'))
    return directory_name


def list_user_stories(username):
    my_bucket = s3_resource.Bucket(BUCKET_NAME)
    file_objs = my_bucket.objects.all()
    file_names = [file_obj.key for file_obj in file_objs]
    files = list(filter(lambda x: x.startswith(username + "/") and x.endswith(".txt"), file_names))
    return list(map(lambda x: x[x.find("/") + 1:].replace(".txt", ""), files))


def story_name_exists(username, story_name):
    user_stories = list_user_stories(username)
    return (username + '/' + story_name + ".txt") in user_stories


def save_story(username, story_name, story_text):
    directory = create_directory(username)
    if story_name_exists(username, story_name):
        raise RuntimeError("Story Name Already Exists")
    s3.put_object(Bucket=BUCKET_NAME, Key=(directory + story_name + ".txt"), Body=story_text)


def get_story_text(username, story_name):
    obj = s3_resource.Object(BUCKET_NAME, username + "/" + story_name + ".txt")
    story_text = obj.get()['Body'].read()
    return story_text


# save_story("koka", "Ertxel trakshi", "Amovida xeebi da gadaiwva tyeebi")
# user_stories = list_user_stories("koka")