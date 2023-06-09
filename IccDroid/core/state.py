import hashlib

from configure import Configuration
from core.action import Action
from core.view import View
from util.util import Util

"""
Record the information of the app's state
"""


class State(object):

    def __init__(self, lines):
        self.lines = lines
        self.classname_list = []
        self.resourceid_list = []
        self.num_list = []
        self.all_views = self.get_view()
        self.all_actions = self.get_all_actions()
        self.type_hash = self.get_type_md5()

        # build graph structure [(a_i,s_i+1,d_i)]
        self.transitions = []

    def get_type_md5(self):
        content = ""
        for i in range(0, len(self.classname_list)):
            content += self.classname_list[i]
        md5_value = hashlib.md5(content.encode('utf8')).hexdigest()
        return md5_value

    def get_instance(self, view):
        # get_instance
        flag = False
        i = 0
        while i < len(self.classname_list):
            if self.classname_list[i] == view.className and self.resourceid_list[i] == view.resourceId:
                flag = True
                self.num_list[i] = self.num_list[i] + 1
                view.set_instance(self.num_list[i])
                break
            i = i + 1
        if flag == False:
            self.classname_list.append(view.className)
            self.resourceid_list.append(view.resourceId)
            self.num_list.append(0)
            view.set_instance(0)
        return view

    def get_view(self):
        all_views = []
        stack = []
        for line in self.lines:
            if '<node ' in line and '/>' in line:
                if len(stack) == 0:
                    view = View(line, None, [])
                else:
                    view = View(line, stack[len(stack) - 1], [])
                    stack[len(stack) - 1].add_son(view)
                view = self.get_instance(view)
                all_views.append(view)
            elif '<node ' in line:
                if len(stack) == 0:
                    view = View(line, None, [])
                else:
                    view = View(line, stack[len(stack) - 1], [])
                view = self.get_instance(view)
                stack.append(view)
            elif '</node>' in line:
                view = stack[len(stack) - 1]
                stack.pop()
                view = self.get_instance(view)
                all_views.append(view)
                if len(stack) > 0:
                    stack[len(stack) - 1].add_son(view)
        return all_views

    # consider ui action (scroll belong to system action)
    def get_all_actions(self):
        actions = []
        action_id = 0
        click_classname_lists = ["android.widget.RadioButton", "android.view.View", "android.widget.ImageView",
                                 "android.widget.View", "android.widget.CheckBox", "android.widget.Button",
                                 "android.widget.Switch", "android.widget.ImageButton", "android.widget.TextView",
                                 "android.widget.CheckedTextView", "android.widget.TableRow", "android.widget.EditText",
                                 "android.support.v7.widget.ar"]
        for view in self.all_views:
            if view.ymax <= Configuration.DEVICE_SCREEN_HEIGHT * 0.0375:  # exclude the event in top 0.0375 of height
                continue
            # exclude system (home/recent_apps) action
            if view.package == "com.android.systemui": # and view.resourceId in ["com.android.systemui:id/back", "com.android.systemui:id/recent_apps","com.android.systemui:id/home"]:
                continue
            # click action
            if view.className in click_classname_lists:
                click_action = Action(view, Configuration.ACTION_TYPE_CLICK, None, action_id)
                action_id += 1
                actions.append(click_action)
            # long-click action
            if view.className in click_classname_lists and (view.longClickable == "true" or view.clickable == "true"):
                longclick_action = Action(view, Configuration.ACTION_TYPE_LONGCLICK, None, action_id)
                action_id += 1
                actions.append(longclick_action)
            # edit action
            if view.className == "android.widget.EditText":
                edit_action = Action(view, Configuration.ACTION_TYPE_EDIT, Util.random_text(), action_id)
                action_id += 1
                actions.append(edit_action)
        return actions
