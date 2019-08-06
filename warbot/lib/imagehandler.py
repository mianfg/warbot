#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WarBotImageHandler
==================

This module generates images.

"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2019, Bloomgogo"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "GPL"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "mianfg@bloomgogo.com"
__status__      = "Production"



# Python Image Library
from PIL import Image, ImageOps, ImageDraw, ImageFont
import random

from vars import route


class WarBotImageHandler:
    """
    Class used to generate images

    ...

    Attributes
    ----------
    battlepics : list<dict>
        List of battlepics, dictionaries with the following keys:
            filename :      filename of battlepic's template
            img1_size :     size of first image
            img1_offset :   offset of first image
            img2_size :     size of second image
            img2_offset :   offset of second image
    newfighterpic : str
        Filename of newfighterpic's template
    alivefighterspic : str
        Filename of alivefighterspic's template
    font_sansserif : str
        Filename of font

    Methods
    -------
    generate_battle(image1, image2, output)
        Generates battle result image
    generate_newfighter(image, output)
        Generates new user image
    generate_alive(image, output)
        Generates image with list of users
    """

    def __init__(self, images_route, resources_route, store_route):
        """
        Parameters
        ----------
        images_route : str
            Folder route to images.
                To avoid bugs, must be absolute path
        resources_route : str
            Folder route to templates.
                To avoid bugs, must be absolute path
        store_route : str
            Folder route to store images.
                To avoid bugs, must be absolute path
        """

        self.images_route = images_route
        self.resources_route = resources_route
        self.store_route = store_route

        self.profile_pic_error = "ih_profilepic.png"

        self.battlepics = [
            # {
            #     'filename':     "ih_battlepic.png",
            #     'img1_size':    (500,500),
            #     'img1_offset':  (360,230),
            #     'img2_size':    (500,500),
            #     'img2_offset':  (1060,230)
            # },
            {
                'filename':     "ih_battlepic_001.png",
                'img1_size':    (229,229),
                'img1_offset':  (726,94),
                'img2_size':    (243,243),
                'img2_offset':  (247,314)
            },
            {
                'filename':     "ih_battlepic_002.png",
                'img1_size':    (198,198),
                'img1_offset':  (179,111),
                'img2_size':    (198,198),
                'img2_offset':  (572,31)
            },
            {
                'filename':     "ih_battlepic_003.png",
                'img1_size':    (146,146),
                'img1_offset':  (714,250),
                'img2_size':    (146,146),
                'img2_offset':  (787,447)
            },
            {
                'filename':     "ih_battlepic_004.png",
                'img1_size':    (271,271),
                'img1_offset':  (927,23),
                'img2_size':    (271,271),
                'img2_offset':  (319,30)
            },
            {
                'filename':     "ih_battlepic_005.png",
                'img1_size':    (265,265),
                'img1_offset':  (693,-10),
                'img2_size':    (218,218),
                'img2_offset':  (-14,32)
            },
            {
                'filename':     "ih_battlepic_006.png",
                'img1_size':    (420,420),
                'img1_offset':  (312,-20),
                'img2_size':    (420,420),
                'img2_offset':  (919,91)
            },
            {
                'filename':     "ih_battlepic_007.png",
                'img2_size':    (438,438),
                'img2_offset':  (514,112),
                'img1_size':    (297,297),
                'img1_offset':  (1137,46)
            },
            {
                'filename':     "ih_battlepic_008.png",
                'img1_size':    (70,70),
                'img1_offset':  (295,101),
                'img2_size':    (83,83),
                'img2_offset':  (683,315)
            },
            {
                'filename':     "ih_battlepic_009.png",
                'img1_size':    (150,150),
                'img1_offset':  (247,5),
                'img2_size':    (232,232),
                'img2_offset':  (472,126)
            },
            {
                'filename':     "ih_battlepic_010.png",
                'img1_size':    (132,132),
                'img1_offset':  (898,53),
                'img2_size':    (132,132),
                'img2_offset':  (296,84)
            },
            {
                'filename':     "ih_battlepic_011.png",
                'img1_size':    (105,105),
                'img1_offset':  (191,2),
                'img2_size':    (105,105),
                'img2_offset':  (281,74)
            },
            {
                'filename':     "ih_battlepic_012.png",
                'img1_size':    (221,221),
                'img1_offset':  (577,62),
                'img2_size':    (272,272),
                'img2_offset':  (106,33)
            },
            {
                'filename':     "ih_battlepic_014.png",
                'img1_size':    (265,265),
                'img1_offset':  (115,78),
                'img2_size':    (350,350),
                'img2_offset':  (412,484)
            },
            {
                'filename':     "ih_battlepic_015.png",
                'img1_size':    (58,58),
                'img1_offset':  (252,65),
                'img2_size':    (58,58),
                'img2_offset':  (332,60)
            }
        ]
        self.newfighterpics = [
            {
                'filename':     "ih_newfighterpic.png",
                'img_size':     (500,500),
                'img_offset':   (710,230)
            }
        ]
        self.alivefighterspic = 'ih_alivefighterspic.png'
        self.winneruserpic = {
            'filename':     "ih_winneruserpic.png",
            'img_size':     (400,400),
            'img_offset':   (750,230)
        }
        self.font_sansserif = 'font_sansserif.ttf'


    def generate_battle(self, image1, image2, output):
        """Generates battle result image

        Generates battle result image out of the battlepics attribute. See
        `self.battlepics` for more info.

        Parameters
        ----------
        image1 : str
            Filename of first user's profile pic (winner).
                File will be retrieved from self.store_route/image1
        image2 : str
            Filename of second user's profile pic (defeated).
                File will be retrieved from self.store_route/image2
        output : str
            Filename for output.
                It will be stored on self.store_route/output
        
        Return
        ------
        str
            Absolute route to generated image
        """

        # retrieve a random battlepic from the list of battlepics
        battlepic = random.choice(self.battlepics)

        # create masks for profile pics
        mask1 = Image.new('L', battlepic['img1_size'], 0)
        draw1 = ImageDraw.Draw(mask1) 
        draw1.ellipse((0, 0) + battlepic['img1_size'], fill=255)
        mask2 = Image.new('L', battlepic['img2_size'], 0)
        draw2 = ImageDraw.Draw(mask2) 
        draw2.ellipse((0, 0) + battlepic['img2_size'], fill=255)

        # open profile pics
        try:
            img1 = Image.open(route.paste(self.images_route, image1), 'r')
        except Exception:
            img1 = Image.open(route.paste(self.resources_route, self.profile_pic_error), 'r')
        try:
            img2 = Image.open(route.paste(self.images_route, image2), 'r')
        except Exception:
            img2 = Image.open(route.paste(self.resources_route, self.profile_pic_error), 'r')
        img1 = img1.resize(battlepic['img1_size'])
        img2 = img2.resize(battlepic['img2_size'])

        # crop profile pics to mask
        img1 = ImageOps.fit(img1, mask1.size, centering=(0.5, 0.5))
        img1.putalpha(mask1)
        img2 = ImageOps.fit(img2, mask2.size, centering=(0.5, 0.5))
        img2.putalpha(mask2)

        # open battlepic template background
        background = Image.open(route.paste(self.resources_route, \
            battlepic['filename']), 'r')

        # paste cropped profile pics
        background.paste(img1, battlepic['img1_offset'], img1)
        background.paste(img2, battlepic['img2_offset'], img2)

        # save battlepic
        output_route = route.paste(self.store_route, output)
        background.save(output_route)

        return output_route
    

    def generate_newfighter(self, image, output):
        """Generates new user image

        Generates new user image out of the newfighterpics attribute. See
        `self.newfighterpics` for more info.

        Parameters
        ----------
        image : str
            Filename of user's profile pic
        output : str
            Filename for output
        
        Return
        ------
        str
            Absolute route to generated image
        """

        # retrieve a random newfighterpic from the list of newfighterpics
        newfighterpic = random.choice(self.newfighterpics)

        # open profile pic
        mask = Image.new('L', newfighterpic['img_size'], 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + newfighterpic['img_size'], fill=255)

        # crop profile pic to mask
        img = Image.open(route.paste(self.images_route, image), 'r')
        img = img.resize(newfighterpic['img_size'])
        img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        img.putalpha(mask)

        # open newfighterpic template background
        background = Image.open(route.paste(self.resources_route, \
            newfighterpic['filename']), 'r')

        # paste cropped profile pic
        background.paste(img, newfighterpic['img_offset'], img)

        # save newfighterpic
        output_route = route.paste(self.store_route, output)
        background.save(output_route)

        return output_route
    

    def generate_alive(self, users, output):
        """Generates image with list of fighters

        Parameters
        ----------
        users : list<dict>
            List of usernames to include, generated from
            WarBot.get_fighters_extended()
        output : str
            Filename for output
        
        Important note
        --------------
        This image will show up to 100 usernames

        Return
        ------
        str
            Absolute route to generated image
        """

        img = Image.open(route.paste(self.resources_route, \
            self.alivefighterspic), 'r')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(route.paste(self.resources_route, \
            self.font_sansserif), 30)
        text = ""
        for i in range (0,6):
            c = 0
            for _ in range(0,20):
                if len(users) > 0:
                    if users[0]['show']:
                        text = "@{}\n".format(users[0]["username"])
                        if users[0]["alive"]:
                            color = (0,0,0)
                        else:
                            color = (170,0,0)
                        draw.text((70+300*i,240+40*c), text, color, font=font)
                        c += 1
                    users.pop(0)
        
        output_route = route.paste(self.store_route, output)
        img.save(output_route)

        return output_route
    

    def generate_winner(self, image, output):
        """Generates winner image

        Generates winner image out of the winneruserpic attribute. See
        `self.winneruserpic` for more info.

        Parameters
        ----------
        image : str
            Filename of user's profile pic
        output : str
            Filename for output
        
        Return
        ------
        str
            Absolute route to generated image
        """

        # open profile pic
        mask = Image.new('L', self.winneruserpic['img_size'], 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + self.winneruserpic['img_size'], fill=255)

        # crop profile pic to mask
        img = Image.open(route.paste(self.images_route, image), 'r')
        img = img.resize(self.winneruserpic['img_size'])
        img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        img.putalpha(mask)

        # open winneruserpic template background
        background = Image.open(route.paste(self.resources_route, \
            self.winneruserpic['filename']), 'r')

        # paste cropped profile pic
        background.paste(img, self.winneruserpic['img_offset'], img)

        # save winneruserpic
        output_route = route.paste(self.store_route, output)
        background.save(output_route)

        return output_route