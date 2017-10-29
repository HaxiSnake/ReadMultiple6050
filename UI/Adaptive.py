# -*- coding: utf-8 -*-

import platform

g_systemName = platform.system()
g_systemInfo = platform.platform()
g_pyVersion = platform.python_version()
size_dict = dict()

# System will be Linux and python == 2.7
if g_systemName == "Linux" and g_pyVersion[:3] == "2.7":
    if "Ubuntu" in g_systemInfo:
        size_dict = {
                        "list_box_height": 20,
                        "send_text_height": 12,
                        "receive_text_height": 15,
                        "reset_label_width": 24,
                        "clear_label_width": 22
                    }

    # raspberry pi
    elif "armv6l" in g_systemInfo:
        size_dict = {
                        "list_box_height": 19,
                        "send_text_height": 12,
                        "receive_text_height": 15,
                        "reset_label_width": 24,
                        "clear_label_width": 22
                    }
else:
    if g_systemInfo[:9]== "Windows-8":
        size_dict = {
                        "list_box_height": 14,
                        "send_text_height": 6,
                        "receive_text_height": 18,
                        "reset_label_width": 7,
                        "clear_label_width": 5
                     }

    elif g_systemInfo[:9]== "Windows-7":
        size_dict = {
                        "list_box_height": 13,
                        "send_text_height": 12,
                        "receive_text_height": 15,
                        "reset_label_width": 7,
                        "clear_label_width": 5
                     }

    elif g_systemInfo[:10]== "Windows-XP":
        size_dict = {
                        "list_box_height": 20,
                        "send_text_height": 12,
                        "receive_text_height": 22,
                        "reset_label_width": 7,
                        "clear_label_width": 5
                     }

    elif g_systemInfo[:10]== "Windows-10":
        size_dict = {
                        "list_box_height": 14,
                        "send_text_height": 6,
                        "receive_text_height": 18,
                        "reset_label_width": 7,
                        "clear_label_width": 5
                     }
    

# font
monaco_font = ('Monaco', 12)