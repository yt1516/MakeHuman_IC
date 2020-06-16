#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    https://bitbucket.org/MakeHuman/makehuman/

**Authors:**           Joel Palmius, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2017

**Licensing:**         AGPL3

    This file is part of MakeHuman (www.makehuman.org).

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


Abstract
--------

TODO
"""

# We need this for gui controls
import camera
from OpenGL.GL import *
import numpy as np

import datetime
import time
import gui3d
import mh
import gui
import log
import getpath
import os
import humanmodifier
import modifierslider
# import algos3d
import json
# import scene
# import projection
import glmodule
import image
from image import Image
import image_operations as imgop
# import guirender
from core import G
from progress import Progress


class FACSslider(object):

      def __init__(self, slider, labelSlider, slidersValues, label_create):

          @slider.mhEvent
          def onChange(value):
              #log.message('toto %s %s %s', labelSlider, slider, slidersValues)
              labelSlider.setTextFormat( 'Intensity: %.2f%%', value*100)
              slidersValues[label_create] = value

class ExampleTaskView(gui3d.TaskView):

    def __init__(self, category, appFacs):
        gui3d.TaskView.__init__(self, category, 'Pain Face Generator')
        self.facs_human = appFacs.selectedHuman
        camera = G.app.modelCamera
        self.app = appFacs

        # self.targets_path_emotions_blender = getpath.getPath('data/FACSHuman/00 Emotions')
        self.targets_path_upper_face = getpath.getPath('data/FACSHuman/01 Upper Face AUs')
        self.targets_path_lower_face = getpath.getPath('data/FACSHuman/02 Lower Face AUs')
        self.targets_path_lip_jaw = getpath.getPath('data/FACSHuman/03 Lip Parting and Jaw Opening')
        # self.targets_path_eye = getpath.getPath('data/FACSHuman/04 Eye Positions')
        # self.targets_path_head = getpath.getPath('data/FACSHuman/05 Head Positions')
        # self.targets_path_misc = getpath.getPath('data/FACSHuman/06 Miscellaneous AUs')

        self.last_directory_rendering = ''
        self.images_to_convert = ''
        self.video_destination = ''
        #self.video_background = 'black.jpg'
        self.renderingWidth = '500'
        self.renderingHeight = '500'
        self.images_set_dir_destination = ''

        # box_emotions_blender = self.addLeftWidget(gui.GroupBox('Emotions blender'))
        box_upper = self.addLeftWidget(gui.GroupBox('Upper Face AUs'))
        box_lower = self.addLeftWidget(gui.GroupBox('Lower Face AUs'))
        # box_head = self.addLeftWidget(gui.GroupBox('Head Positions'))
        # box_eye = self.addLeftWidget(gui.GroupBox('Eye Positions'))
        box_lip = self.addLeftWidget(gui.GroupBox('Lip Parting and Jaw Opening'))
        # box_misc = self.addLeftWidget(gui.GroupBox('Miscellaneous AUs'))
        box_weight = self.addRightWidget(gui.GroupBox('AU Matrix Weights'))
        box_gen = self.addRightWidget(gui.GroupBox('View and Generate Images'))
        box_tools = self.addRightWidget(gui.GroupBox('Tools'))
        # box_aus_code = self.addRightWidget(gui.GroupBox('Action Units coding'))

        # self.general_intensity = box_aus_code.addWidget(gui.Slider(value=100, min=0, max=100, label=['General Intensity : ','%d%%']), columnSpan = 2)
        # #self.general_intensity_progress_bar = box_tools.addWidget(gui.ProgressBar())
        # #self.general_intensity_progress_bar.setProgress(1)
        # self.txt_file_loaded = box_aus_code.addWidget(gui.TextView('- New facial code -'), columnSpan = 2)
        # self.load_facs_button = box_aus_code.addWidget(gui.BrowseButton('open', "Load FACS Code"), 3, 0)
        # self.save_facs_button = box_aus_code.addWidget(gui.BrowseButton('save', "Save FACS Code"), 3, 1)
        # # self.save_target_button = box_aus_code.addWidget(gui.BrowseButton('save', "Save target"))
        # self.generate_au_coding_button = box_aus_code.addWidget(gui.Button('Get AU\'s Code'), columnSpan = 2)
        # self.txt_coding = box_aus_code.addWidget(gui.TextView('AU\'s code generated :'), columnSpan = 2)
        # self.au_coding = box_aus_code.addWidget(gui.DocumentEdit(text='Neutral'), columnSpan = 2)
        # self.one_shot_button = box_tools.addWidget(gui.Button('Take one shot'), 1, 0)

        self.survey_img_button=box_weight.addWidget(gui.Button('Generate Survey Images'), columnSpan = 2)
        self.au4_lab=box_weight.addWidget(gui.TextView('AU4 Weight'))
        self.au4_val=box_weight.addWidget(gui.TextEdit(text='0.8865'))
        self.au7_lab=box_weight.addWidget(gui.TextView('AU7 Weight'))
        self.au7_val=box_weight.addWidget(gui.TextEdit(text='0.7758'))
        self.au9_lab=box_weight.addWidget(gui.TextView('AU9 Weight'))
        self.au9_val=box_weight.addWidget(gui.TextEdit(text='2.6129'))
        self.au10_lab=box_weight.addWidget(gui.TextView('AU10 Weight'))
        self.au10_val=box_weight.addWidget(gui.TextEdit(text='3.6517'))

        self.reset_camera_button = box_gen.addWidget(gui.Button('Full face camera view'), columnSpan = 2)
        self.master_slider = box_gen.addWidget(gui.Slider(value=0, min=0, max=100, label=['General Intensity : ','%d%%']), columnSpan = 2)
        self.one_shot_button = box_gen.addWidget(gui.Button('Take one shot'), columnSpan = 2)
        self.generate_set_button = box_gen.addWidget(gui.Button('generate pain image set'), columnSpan = 2)

        self.one_shot_stereo_button = box_tools.addWidget(gui.Button('Stereoscopic shot'), columnSpan = 2)
        self.au_set_gen_button = box_tools.addWidget(gui.BrowseButton('open', "Dir to img"), 2, 0)
        self.material_gen_button = box_tools.addWidget(gui.BrowseButton('open', "Images set"), 2, 1)
        self.material_gen_dir_button = box_tools.addWidget(gui.FileEntryView('Browse', mode='dir'), columnSpan = 2)
        self.camera_slider_x = box_tools.addWidget(gui.Slider(value=0, min=-1, max=1, label=['camera x: ','%2f']), columnSpan = 2)
        self.camera_slider_y = box_tools.addWidget(gui.Slider(value=0, min=-1, max=1, label=['camera y: ','%2f']), columnSpan = 2)
        self.camera_slider_zoom = box_tools.addWidget(gui.Slider(value=0, min=4, max=9, label=['Zoom: ','%2f']), columnSpan = 2)
        self.rotation_slider_z = box_tools.addWidget(gui.Slider(value=0, min=-90, max=90, label=['rotation z: ','%2f']), columnSpan = 2)
        self.reset_button = box_tools.addWidget(gui.Button('Reset Facial Code'), columnSpan = 2)
        self.full_set_button = box_tools.addWidget(gui.Button('Full set generation'), columnSpan = 2)
        self.facsvatar_set_button = box_tools.addWidget(gui.BrowseButton('open', 'FACAvatar rendering'), columnSpan = 2)

        self.facs_code_names_path = getpath.getDataPath('FACSHuman')
        self.facs_code_names_file = self.facs_code_names_path + '/au.json'
        self.facs_code_names = json.loads(open(self.facs_code_names_file).read())

        self.slidersValues = {} #Keep a trace of values in the General intensity sliders function
        self.sliders = {}
        self.sliders_order = []
        self.labelSlider = {}
        #self.modifiers = {}
        self.au_timeline_values = {} # For the animation functionality
        self.au_facs_loaded_file_values = {} # For the animation functionality

        self.facs_code_names_path = getpath.getDataPath('FACSHuman')
        self.facs_code_names_file = self.facs_code_names_path + '/au.json'
        self.facs_code_names = json.loads(open(self.facs_code_names_file).read())

        # self.searchTargets(self.targets_path_emotions_blender, box_emotions_blender, 'Emotions Blender')
        self.searchTargets(self.targets_path_upper_face, box_upper, 'Upper Face AUs')
        self.searchTargets(self.targets_path_lower_face, box_lower, 'Lower Face AUs')
        self.searchTargets(self.targets_path_lip_jaw, box_lip, 'Lip Parting and Jaw Opening')
        # self.searchTargets(self.targets_path_eye, box_eye, 'Eye Positions')
        # self.searchTargets(self.targets_path_head, box_head, 'Head Positions')
        # self.searchTargets(self.targets_path_misc, box_misc, 'Miscellaneous AUs')



        @self.camera_slider_x.mhEvent
        def onChanging(value):
            pos = self.facs_human.getPosition()
            pos[0] = value
            self.facs_human.setPosition(pos)
            mh.redraw()

        @self.camera_slider_y.mhEvent
        def onChanging(value):
            pos = self.facs_human.getPosition()
            pos[1] = value
            self.facs_human.setPosition(pos)
            mh.redraw()

        @self.camera_slider_zoom.mhEvent
        def onChanging(value):
            camera.setZoomFactor(value)

        @self.rotation_slider_z.mhEvent
        def onChanging(value):
            pos = self.facs_human.getRotation()
            pos[1] = value
            self.facs_human.setRotation(pos)
            mh.redraw()


##########################################################################
# Generate all AUs images
##########################################################################

        @self.facsvatar_set_button.mhEvent
        def onClicked(path):
            self.generateFacsvatarDirSet(path)

##########################################################################
# Generate all AUs images
##########################################################################

        @self.au_set_gen_button.mhEvent
        def onClicked(path):
            self.generateDirSet(path)

##########################################################################
# Generate material images
##########################################################################

        @self.material_gen_button.mhEvent
        def onClicked(path):
            self.generateCompleteImagesSetFromDir(path)
##########################################################################
# Generate material images
##########################################################################

        @self.material_gen_dir_button.mhEvent
        def onFileSelected(event):
            # self.images_set_dir_destination = os.path.dirname(path)
            self.images_set_dir_destination = event.path
            # self.images_set_dir_destination = os.path.dirname(path)
            gui3d.app.statusPersist('Images destination : ' + str(self.images_set_dir_destination))


##########################################################################
# Reset button for camera's orientation to have full face view
# in order to have constant point of view for experiments
##########################################################################

        @self.reset_camera_button.mhEvent
        def onClicked(event):
            gui3d.app.setTargetCamera(131, 9, False)
            gui3d.app.axisView([0.0, 0.0, 0.0])
            pos = [0, 0.2, 0]
            self.facs_human.setPosition(pos)
            self.camera_slider_x.setValue(0)
            self.camera_slider_y.setValue(0.2)
            self.camera_slider_zoom.setValue(9)
            self.rotation_slider_z.setValue(0)
            self.rotation_slider_z.onChanging(0)
            self.rotation_slider_z.update()
            mh.redraw()
            gui3d.app.statusPersist('Camera updated')

        @self.one_shot_button.mhEvent
        def onClicked(event):
            self.renderFacsPicture()

##########################################################################
# Reset facial code and AUs button
##########################################################################

        @self.reset_button.mhEvent
        def onClicked(event):
            G.app.prompt('Confirmation',
                    'Do you really want to reset your Facial code ?',
                    'Yes', 'Cancel', self.resetFacialCodes)

##########################################################################
# Generate 81 images for the survey website
##########################################################################
        @self.survey_img_button.mhEvent
        def onClicked(event):
            weight=[0,0.5,1]
            for i4 in range(3):
                for i7 in range(3):
                    for i9 in range(3):
                        for i10 in range(3):
                            self.survey_img_gen(weight[i4],weight[i7],weight[i9],weight[i10])
                            time.sleep(0.5)
                            self.renderSurveyImg(i4,i7,i9,i10)

##########################################################################
# Generate and save 101 images for overall intensity = 0% to 100%
##########################################################################
        @self.generate_set_button.mhEvent
        def onClicked(event):
            for val in range(0,101):
                self.generate_face_set(val)
                time.sleep(0.5)
                self.renderFacsPicture()
##########################################################################
# View pain expression change at various general intensities
##########################################################################
        @self.master_slider.mhEvent
        def onChange(value):
            self.masterslider_render(value, True)

    def survey_img_gen(self,i4,i7,i9,i10):
        for key_code in self.slidersValues.keys():
            if key_code=='4':
                self.sliders[key_code].onChanging(i4)
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            elif key_code=='7':
                self.sliders[key_code].onChanging(i7)
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            elif key_code=='9':
                self.sliders[key_code].onChanging(i9)
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            elif key_code=='10':
                self.sliders[key_code].onChanging(i10)
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            else:
                self.sliders[key_code].onChanging(0)
            self.sliders[key_code].update()
        self.facs_human.applyAllTargets()

    def renderSurveyImg(self, i4,i7,i9,i10,dir_images = None, pic_file = None, pic_file_reverse = None):
       self.facs_human.applyAllTargets()
       self.refreshAuSmoothSetting()

       grabPath = mh.getPath('grab')
       if not os.path.exists(grabPath):
          os.makedirs(grabPath)

       if pic_file is not None:
          dir_pic_file = os.path.join(grabPath, dir_images)
          pic_file = pic_file + '.png'
          pic_file = os.path.join(dir_pic_file, pic_file)
          if pic_file_reverse is not None:
             pic_file_reverse = pic_file_reverse + '.png'
             pic_file_reverse = os.path.join(dir_pic_file, pic_file_reverse)
       else:
           grabName = str(i4)+str(i7)+str(i9)+str(i10)+'.png'
           pic_file = os.path.join(grabPath, grabName)

       if self.renderingWidth == '' or self.renderingHeight == '' :
          G.app.prompt('Warning',
                        'Nothing to render check the image size.',
                        'Ok')
       else:
           img_width, img_height  = 2000,2000#int(self.renderingWidth), int(self.renderingHeight)
           glmodule.draw(False)
           img = glmodule.renderToBuffer(img_width, img_height)
           alphaImg = glmodule.renderAlphaMask(img_width, img_height)
           img = imgop.addAlpha(img, imgop.getChannel(alphaImg, 0))
           img = img.toQImage()
           if pic_file is not None:
               img.save(pic_file)
               log.message("Image saved to %s", pic_file)
           if pic_file_reverse is not None:
               img.save(pic_file_reverse)
               log.message("Image saved to %s", pic_file_reverse)
           del alphaImg
           del img

           gui3d.app.statusPersist("Image saved to %s", pic_file)

    def generate_face_set(self,val):
        multiplier=float(val)/200
        au4=float(self.au4_val.getText())
        au7=float(self.au7_val.getText())
        au9=float(self.au9_val.getText())
        au10=float(self.au10_val.getText())
        beta=[au4,au7,au9,au10]
        weight=[1+i/max(beta) for i in beta]

        for key_code in self.slidersValues.keys():
            if key_code=='4':
                self.sliders[key_code].onChanging(multiplier*weight[0])
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            elif key_code=='7':
                self.sliders[key_code].onChanging(multiplier*weight[1])
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            elif key_code=='9':
                self.sliders[key_code].onChanging(multiplier*weight[2])
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            elif key_code=='10':
                self.sliders[key_code].onChanging(multiplier*weight[3])
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            else:
                self.sliders[key_code].onChanging(0)
            self.sliders[key_code].update()
        self.facs_human.applyAllTargets()

    def masterslider_render(self, general_intensity_value, general_intensity_slider = False):
        multiplier=float(general_intensity_value)/200
        au4=float(self.au4_val.getText())
        au7=float(self.au7_val.getText())
        au9=float(self.au9_val.getText())
        au10=float(self.au10_val.getText())

        beta=[au4,au7,au9,au10]

        weight=[1+i/max(beta) for i in beta]

        for key_code in self.slidersValues.keys():
            if key_code=='4':
                self.sliders[key_code].onChanging(multiplier*weight[0])
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            elif key_code=='7':
                self.sliders[key_code].onChanging(multiplier*weight[1])
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            elif key_code=='9':
                self.sliders[key_code].onChanging(multiplier*weight[2])
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            elif key_code=='10':
                self.sliders[key_code].onChanging(multiplier*weight[3])
                self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            else:
                self.sliders[key_code].onChanging(0)
            self.sliders[key_code].update()
        self.facs_human.applyAllTargets()
        if general_intensity_slider:
           self.refreshAuSmoothSetting()

    def renderFacsPicture(self, dir_images = None, pic_file = None, pic_file_reverse = None):
       self.facs_human.applyAllTargets()
       self.refreshAuSmoothSetting()

       grabPath = mh.getPath('grab')
       if not os.path.exists(grabPath):
          os.makedirs(grabPath)

       if pic_file is not None:
          dir_pic_file = os.path.join(grabPath, dir_images)
          pic_file = pic_file + '.png'
          pic_file = os.path.join(dir_pic_file, pic_file)
          if pic_file_reverse is not None:
             pic_file_reverse = pic_file_reverse + '.png'
             pic_file_reverse = os.path.join(dir_pic_file, pic_file_reverse)
       else:
           grabName = datetime.datetime.now().strftime('grab_%Y-%m-%d_%H.%M.%S.png')
           pic_file = os.path.join(grabPath, grabName)


       if self.renderingWidth == '' or self.renderingHeight == '' :
          G.app.prompt('Warning',
                        'Nothing to render check the image size.',
                        'Ok')
       else:
           img_width, img_height  = 2000,2000#int(self.renderingWidth), int(self.renderingHeight)
           glmodule.draw(False)
           img = glmodule.renderToBuffer(img_width, img_height)
           alphaImg = glmodule.renderAlphaMask(img_width, img_height)
           img = imgop.addAlpha(img, imgop.getChannel(alphaImg, 0))
           img = img.toQImage()
           if pic_file is not None:
               img.save(pic_file)
               log.message("Image saved to %s", pic_file)
           if pic_file_reverse is not None:
               img.save(pic_file_reverse)
               log.message("Image saved to %s", pic_file_reverse)
           del alphaImg
           del img

           gui3d.app.statusPersist("Image saved to %s", pic_file)

    def refreshAuSmoothSetting(self):
        if self.facs_human.isSubdivided():
            self.facs_human.setSubdivided(False)
            self.facs_human.setSubdivided(True)

    def resetFacialCodes(self, erase_all='True'):
        progress_reset_button = Progress(len(self.sliders))
        was_subdivided = False
        if self.facs_human.isSubdivided():
            was_subdivided = True
            self.facs_human.setSubdivided(False)
        for aSlider in self.sliders.keys():
            #if self.slidersValues[aSlider] >= 0:
            self.sliders[aSlider].resetValue()
            self.sliders[aSlider].update()
            self.slidersValues[aSlider] = 0
            self.labelSlider[aSlider].setTextFormat('Intensity: 0%%')
            gui3d.app.statusPersist('Reseting : ' + aSlider)
            progress_reset_button.step()

        if erase_all:
           self.au_timeline_values = {}
           self.au_facs_loaded_file_values = {}
           self.txt_animatiom_file_loaded.setText('No animation file loaded')

        self.animation_test.onChange(0)
        self.animation_test.update()
        self.animation_test.setValue(0)

        self.general_intensity.onChange(100)
        self.general_intensity.update()
        self.general_intensity.setValue(100)

        self.au_coding.setText('Neutral')
        self.txt_file_loaded.setText('- New facial code -')
        self.facs_human.applyAllTargets()
        # self.refreshAuSmoothSetting()
        if was_subdivided == True:
            self.facs_human.setSubdivided(True)
        gui3d.app.statusPersist('Reset is done, now in neutral facial expression setting')

    def generateFacsvatarDirSet(self, path):
        dir_list = os.path.dirname(path)

        for root, dirs, files in os.walk(dir_list):
            progress_render_images = Progress(len(files))
            for f in files:
                if f.endswith(".json"):
                   self.resetFacialCodes()
                   self.loadFacsVatarFile(os.path.join(root, f))
                   self.renderFacsPicture(dir_list, f.split(".")[0])
                progress_render_images.step()

    def generateDirSet(self, path):
        dir_list = os.path.dirname(path)

        for root, dirs, files in os.walk(dir_list):
            progress_render_images = Progress(len(files))
            for f in files:
                if f.endswith(".facs"):
                   self.resetFacialCodes()
                   self.loadFacsFile(os.path.join(root, f))
                   self.renderFacsPicture(dir_list, f.split(".")[0])
                progress_render_images.step()

    def renderImagesSet(self, timeline=False, dir_destination = None, dir_name = None):
        nb_images = int(self.images_number_to_render.getText())
        if nb_images > 0:
           #gui3d.app.statusPersist('%s %s', self.images_number_to_render.getText(), type(nb_images))
           if dir_destination is None:
              if self.images_set_dir_destination != '':
                 dir_images_path = self.images_set_dir_destination
                 dir_images = datetime.datetime.now().strftime('images_%Y-%m-%d_%H_%M_%S')
              else:
                dir_images = datetime.datetime.now().strftime('images_%Y-%m-%d_%H_%M_%S')
                dir_images_path = mh.getPath('grab')
           else:
              dir_images = dir_name
              dir_images_path = dir_destination


           self.last_directory_rendering = dir_images_path + '/' + dir_images
           dir_images_path = os.path.join(dir_images_path, dir_images)

           if not os.path.exists(dir_images_path):
              os.makedirs(dir_images_path)

           nb_image_neutral_timeline_start = int(self.images_number_neutral_to_anim_start.getText())
           nb_image_neutral_timeline_stop  = int(self.images_number_neutral_to_anim_stop.getText())


           if self.render_timelined_video_chekbox.selected and self.scene_reverse_chekbox.selected and len(self.au_timeline_values) > 0:

              self.resetFacialCodes(False)
              self.sliderIntensitySetFromAnim("start")

              self.generalIntensitySliderRender(0) # self.general_intensity.onChange(0)
              self.renderFacsPicture(dir_images_path, '0')
              progress_render_images = Progress(nb_image_neutral_timeline_start)

              # Render neutral images before timeline
              for i in range(1, nb_image_neutral_timeline_start + 1):
                  value_intensity = i*100/nb_image_neutral_timeline_start
                  self.generalIntensitySliderRender(value_intensity) #self.general_intensity.onChange(value_intensity)
                  gui3d.app.statusPersist("Rendering neutral to animation images %s of %s", i ,nb_image_neutral_timeline_start)
                  picture_name = str(i)
                  self.renderFacsPicture(dir_images_path, picture_name)
                  progress_render_images.step()

              self.generalIntensitySliderRender(100) #self.general_intensity.onChange(100)
              progress_render_images = Progress(nb_images)

              # Render the Timeline
              for i in range(1, nb_images + 1):
                  self.slidersSequencerRenderImageSet(i)
                  gui3d.app.statusPersist("Rendering timeline images %s of %s", i ,nb_images)
                  picture_name = str(i+nb_image_neutral_timeline_start)
                  self.renderFacsPicture(dir_images_path, picture_name)
                  progress_render_images.step()

              self.sliderIntensitySetFromAnim("stop")
              progress_render_images = Progress(nb_image_neutral_timeline_stop)

              # Render neutral images after timeline
              for i in range(nb_images + 1, nb_images + nb_image_neutral_timeline_stop + 1):
                  value_intensity = 100-((i - nb_images + 1)*100)/((nb_images + nb_image_neutral_timeline_stop + 1)-nb_images+1)
                  self.generalIntensitySliderRender(value_intensity) #self.general_intensity.onChange(value_intensity)
                  gui3d.app.statusPersist("Rendering animation to neutral images %s of %s", i - nb_images , nb_image_neutral_timeline_stop)
                  picture_name = str(i + nb_image_neutral_timeline_start)
                  self.renderFacsPicture(dir_images_path, picture_name)
                  progress_render_images.step()
           else:
               progress_render_images = Progress(nb_images)

               if self.render_timelined_video_chekbox.selected :
                  self.resetFacialCodes(False)
               else:
                  self.generalIntensitySliderRender(0) # self.general_intensity.onChange(0)
                  self.renderFacsPicture(dir_images_path, '0')

               for i in range(1, nb_images + 1):

                   if self.render_timelined_video_chekbox.selected :
                      self.slidersSequencerRenderImageSet(i)
                   else:
                       value_intensity = i*100/nb_images
                       self.generalIntensitySliderRender(value_intensity) #self.general_intensity.onChange(value_intensity)

                   picture_name = str(i)

                   if self.scene_reverse_chekbox.selected:
                      picture_name_reverse = str((nb_images*2+1)-i)
                      self.renderFacsPicture(dir_images_path, picture_name, picture_name_reverse)
                   else:
                       self.renderFacsPicture(dir_images_path, picture_name)

                   gui3d.app.statusPersist("Rendering picture %s of %s", i ,nb_images)
                   progress_render_images.step()

           gui3d.app.statusPersist('Rendered images saved in %s', dir_images_path)
        else:
            G.app.prompt('Warning',
                         'Nothing to render check the number of images.',
                         'Ok')

        self.facs_human.applyAllTargets()
        self.refreshAuSmoothSetting()




    def searchTargets(self, facsTargetFolder, boxDestination, boxName):
        au_order_file = facsTargetFolder + '/auorder.json'
        au_order = json.loads(open(au_order_file).read())
       # log.message("au_order %s %s", au_order_file, au_order)
        for the_file_name in au_order:
            file_to_load = os.path.join(facsTargetFolder, the_file_name + '.target')
            self.createTargetControls(boxDestination, file_to_load, facsTargetFolder, boxName)
        self.sliders_order.append(the_file_name)

    def createTargetControls(self, box, targetFile, facsTargetFolder, boxName):
        targetFile = os.path.relpath(targetFile, facsTargetFolder)
        facs_modifier = humanmodifier.SimpleModifier(boxName, facsTargetFolder, targetFile)
        facs_modifier.setHuman(self.facs_human)
        self.label_create = str(facs_modifier.name)
        self.labelSlider[self.label_create] = box.addWidget(gui.TextView("Intensity: 0%"))
        self.slidersValues[self.label_create] = 0
        self.sliders[self.label_create] = box.addWidget(modifierslider.ModifierSlider(modifier=facs_modifier, label=self.facs_code_names[self.label_create]))
       # Create object for mhEvent on sliders to catch values and update labeltxt
        FACSslider(self.sliders[self.label_create], self.labelSlider[self.label_create], self.slidersValues, self.label_create)


    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)
        gui3d.app.statusPersist('FACSHuman a tool to create facial expression based on the Paul Ekman Facial Action Coding System')
        gui3d.app.backplaneGrid.setVisibility(False)
        gui3d.app.backgroundGradient.mesh.setColors([0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0])
    def onHide(self, event):
        gui3d.app.statusPersist('')

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements
def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addTask(ExampleTaskView(category, app))


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass
