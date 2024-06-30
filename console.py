#!/usr/bin/python
"""
    console: represent command shell for interating with storyAfrika

"""

from cmd import Cmd
from models.base_model import BaseModel
from models.story import Story
from models.comment import Comment
from models.user import User
from models.topic import Topic
from models.like import Like
from models.bookmark import Bookmark
from models.follower import Follower
from models.topic_follower import TopicFollower


class StoryAfrikaShell(Cmd):
    prompt = '--> '
    intro = '\nWelcome to story storyAfrika\n'

    def __extract(self, string) -> list:
        """ extracts values separated by space or = sign 
        in a string into a list of strings
            ex: david="asdf" ['david', 'asdf']
        """
        as_array = string.split(" ")  # split words sperated by speces
        as_2darray = [item.split("=") for item in as_array] # split by =
        # replace '""' to '' and "''" to ''
        as_array = [item.replace('"', '') for listitem in as_2darray for item in listitem]
        as_array = [item.replace("'", '') for item in as_array]
        # filter out empty strings

        as_array = [item for item in as_array if item != ""]
        # convert "['1','2']" to ['1', '2']
        for idx, item in enumerate(as_array):
            if item[0] == '[':
                as_array[idx] = eval(item)
                as_array[idx] = [str(item) for item in as_array[idx]]

        return(as_array)


    def __check(self, list_items) -> list:
        """ check if the user pass the command in the following format
                - attribute="value"
                - attribute='value'
        """

        for idx in range(len(list_items)):
            try:
                _ = list_items[idx]

            except IndexError:
                print(idx)
                if idx % 2 == 0:  # even
                    print(f"**{list_items[idx - 2]} or it value is missing**")
                elif idx % 2 == 1:  # odd
                    print(f"**{list_items[idx - 1]} or it value is missing**")
                
                return None
            
            else:
                if idx >= (len(list_items) - 1):
                    list_items[len(list_items):] = []
                print(list_items)
        if list_items == []:
            print(
                f"You did not passed",
                "any attribute along with it value",
                "like so: attribute_name='value'"
            )
            return None
        
        return list_items

    def do_create_user(self, args):
        """ Creates a user
            ex: create_user username="david" email='ex@com' password="xyz1234"
        """

        # convert args to a sepparate list of string
        args_as_array = self.__extract(args)
        
        if self.__check(args_as_array) is None:
            return
        
        _, username, _, email, _, password = args_as_array
        user = User(username=username, email=email, password=password)
        user.save()
        print(user.id)

    def do_create_story(self, args):
        """ Creates a story
            ex: create_story title='love' text='xyz' user_id=1 topics_id=['2','3']
        """

        # convert args to a sepparate list of string
        args_as_array = self.__extract(args)
        print(args_as_array)
        
        
        if self.__check(args_as_array) is None:
            return
        
        _, title, _, text, _, user_id, _, topics_id = args_as_array
        story = Story(title, text, user_id, topics_id)
        story.save()
        print(story.id)

    def do_quit(self, args):
        exit()


if __name__ == '__main__':
    StoryAfrikaShell().cmdloop()
