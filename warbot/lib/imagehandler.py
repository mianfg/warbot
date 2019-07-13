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
    newuserpic : str
        Filename of newuserpic's template
    aliveuserspic : str
        Filename of aliveuserspic's template
    font_sansserif : str
        Filename of font

    Methods
    -------
    generate_battle(image1, image2, output)
        Generates battle result image
    generate_newuser(image, output)
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
                'img1_size':    (255,255),
                'img1_offset':  (712,84),
                'img2_size':    (255,255),
                'img2_offset':  (243,306)
            }
        ]
        self.newuserpics = [
            {
                'filename':     "ih_newuserpic.png",
                'img_size':     (500,500),
                'img_offset':   (710,230)
            }
        ]
        self.aliveuserspic = 'ih_aliveuserspic.png'
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
            Filename of first user's profile pic.
                File will be retrieved from self.store_route/image1
        image2 : str
            Filename of second user's profile pic.
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
        img1 = Image.open(route.paste(self.images_route, image1), 'r')
        img2 = Image.open(route.paste(self.images_route, image2), 'r')
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
    

    def generate_newuser(self, image, output):
        """Generates new user image

        Generates new user image out of the newuserpics attribute. See
        `self.newuserpics` for more info.

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

        # retrieve a random newuserpic from the list of newuserpics
        newuserpic = random.choice(self.newuserpics)

        # open profile pic
        mask = Image.new('L', newuserpic['img_size'], 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + newuserpic['img_size'], fill=255)

        # crop profile pic to mask
        img = Image.open(route.paste(self.images_route, image), 'r')
        img = img.resize(newuserpic['img_size'])
        img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        img.putalpha(mask)

        # open newuserpic template background
        background = Image.open(route.paste(self.resources_route, \
            newuserpic['filename']), 'r')

        # paste cropped profile pic
        background.paste(img, newuserpic['img_offset'], img)

        # save newuserpic
        output_route = route.paste(self.store_route, output)
        background.save(output_route)

        return output_route
    

    def generate_alive(self, users, output):
        """Generates image with list of users

        Parameters
        ----------
        users : list<dict>
            List of usernames to include, generated from
            WarBot.get_users_extended()
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
            self.aliveuserspic), 'r')
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
