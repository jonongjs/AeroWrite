#!/usr/bin/python
# -*- encoding: utf8 -*-

"""Copyright (C) 2013 BARATTERO Laurent
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""

# $Id: $
__author__ = "Laurent Barattero <laurentBa@larueluberlu.net>"
__data__ = " "
__version__= "$Revision: 0.0 $"
__credit__ = " "

"""TODOLIST :
print debug error for .glo files
implement SUB voir comment ameliore le truc grace à un buffer
est ce que ca vaut le coup ?
"""

##### EXECPTION #####

class UCharError(Exception):
  """ exception handling char """
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)


class UInt16Error(Exception):
  """ exception handling uint16 """
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

#---(END OF EXCEPTION)


#############################
# CLASS AEROCHECK           # 
#############################
class AeroCheck(object):
  """check values"""

  TMAX = 65535
  TMIN = 1
  CMAX = 255
  CMIN = 0

  #ct_sec (hundredth seconds)
  @classmethod
  def testUint16(cls, ct_sec):
    try:
      if (ct_sec < cls.TMIN) | (ct_sec  > cls.TMAX):
        raise UInt16Error("in delay -> {} : is not an unsigned int 16".format(str(ct_sec)))
    except UInt16Error as e:
      print("UInt16Error : ", e)


  @classmethod
  def testLoop(cls, nb_loop):
    """ test if Values are betwen 1 and 255 """
    try:
      if (nb_loop < (cls.CMIN + 1)) | (nb_loop > cls.CMAX):
        raise UCharError("in loop -> {} : is not an unsigned char".format(str(nb_loop)))
    except UCharError as e:
      print("UCharError : ", e)

  @classmethod
  def testUchar(cls, R, G, B):
    """ test if Values are betwen 0 and 255 """
    for i in (R, G, B):
      try:
        if (i < cls.CMIN) | (i > cls.CMAX):
          raise UCharError("in a led value -> {} : is not an unsigned char".format(str(i)))
      except UCharError as e:
        print("UCharError : ", e)



#############################
# CLASS COLOR               # 
#############################
class Color(object):
    """
        class Color
    """
    ##### PRIVATE FUNCTIONS #####
    def __init__(self, R=0, G=0, B=0):
        lcol = (R, G, B)
        AeroCheck.testUchar(*lcol)
        self.__R = R
        self.__G = G
        self.__B = B
    #---(END OF PRIVATE FUNCTIONS) 

    def get_R(self):
        return self.__R

    def get_G(self):
        return self.__G

    def get_B(self):
        return self.__B

    def set_R(self, R):
        lcol = (R, 0, 0)
        AeroCheck.testUchar(*lcol)
        self.__R = R

    def set_G(self, G):
        lcol = (0, G, 0)
        AeroCheck.testUchar(*lcol)
        self.__G = G

    def set_B(self,B):
        lcol = (0, 0, B)
        AeroCheck.testUchar(*lcol)
        self.__B = B

    def set_RGB(self, R, G, B):
        lcol = (R, G, B)
        AeroCheck.testUchar(*lcol)
        self.__R = R
        self.__G = G
        self.__B = B

#############################
# CLASS PROPFILE            # 
#############################
class PropFile(object):
  """ class to generate files .glow for props """

  ##### PRIVATE FUNCTIONS #####
  def __init__(self, glo_file):
    try:
      # newline option is for dos file it's not mandatory for linux and mac  
      self.f = open(str(glo_file), 'w', encoding="utf-8", newline='\r\n')
    except IOError: 
      print("can't open file : ", filename)

    self.__buff_sub = ""

  def __del__(self):
    self.f.close()

  def __write_space(self):
    self.f.write(" ")

  def __write_colors(self, R, G, B):
    for i in (R, G, B):
      self.f.write("," + str(i))
    self.__write_space()

  # ...ct_sec (hundredth seconds)
  def __write_ct_sec(self, ct_sec):
      self.f.write("," + str(ct_sec))
      self.__write_space()

  #---(END OF PRIVATE FUNCTIONS)

  #---------------------------
  #   COMMENT FUNCTION        
  #---------------------------
  def cmt(self, cmt):
    """Write comment"""
    self.f.write(";" + str(cmt) + "\n")





#reprendre ici
  #---------------------------
  #   cc CLASICAL FUNCTION    
  #---------------------------
  def cc(self, cls_color, cmt=""):
    """For use C function"""
    lcol = (cls_color.get_R(), cls_color.get_G(), cls_color.get_B()) 
    AeroCheck.testUchar(*lcol)
    self.f.write("C")
    self.__write_colors(*lcol)
    self.cmt(cmt)

  #---------------------------
  #   c CLASICAL FUNCTION    
  #---------------------------
  def c(self, R, G, B, cmt=""):
    """For use C function"""
    lcol = (R, G, B) 
    AeroCheck.testUchar(*lcol)
    self.f.write("C")
    self.__write_colors(*lcol)
    self.cmt(cmt)

  #---------------------------
  #   r CLASICAL FUNCTION     
  #---------------------------
  def r(self, R, cmt=""):
    """For use R function"""
    lcol = (R, 0, 0) 
    AeroCheck.testUchar(*lcol)
    self.f.write("C")
    self.__write_colors(*lcol)
    self.cmt(cmt)


  #---------------------------
  #   G CLASICAL FUNCTION     
  #---------------------------
  def g(self, G, cmt=""):
    """For use G function"""
    lcol = (0, G, 0) 
    AeroCheck.testUchar(*lcol)
    self.f.write("C")
    self.__write_colors(*lcol)
    self.cmt(cmt)

  #---------------------------
  #   B CLASICAL FUNCTION     
  #---------------------------
  def b(self, B, cmt=""):
    """For use B function"""
    lcol = (0, 0, B) 
    AeroCheck.testUchar(*lcol)
    self.f.write("C")
    self.__write_colors(*lcol)
    self.cmt(cmt)

  #---------------------------
  #   D CLASICAL FUNCTION     
  #---------------------------
  def d(self, ct_sec, cmt=""):
    """For use D function"""
    AeroCheck.testUint16(ct_sec)
    self.f.write("D")
    self.__write_ct_sec(ct_sec)
    self.cmt(cmt)
    

  #---------------------------
  #   RAMP CLASICAL FUNCTION 
  #---------------------------
  def ramp(self, R, G, B, ct_sec, cmt=""):
    """For use RAMP function"""
    lcol = (R, G, B) 
    AeroCheck.testUchar(*lcol)
    AeroCheck.testUint16(ct_sec)
    self.f.write("RAMP")
    self.__write_colors(*lcol)
    self.__write_ct_sec(ct_sec)
    self.cmt(cmt)

  #---------------------------
  #   RAMP WITH CLASS COLOR ARGUMENT FUNCTION 
  #---------------------------
  def cramp(self, cls_color, ct_sec, cmt=""):
    """For use RAMP function"""
    lcol = (cls_color.get_R(), cls_color.get_G(), cls_color.get_B()) 
    AeroCheck.testUchar(*lcol)
    AeroCheck.testUint16(ct_sec)
    self.f.write("RAMP")
    self.__write_colors(*lcol)
    self.__write_ct_sec(ct_sec)
    self.cmt(cmt)



  #---------------------------
  #   END CLASICAL FUNCTION 
  #---------------------------
  def end(self):
    """Write END"""
    self.f.write("END\n")
    

  #  (END CLASICAL FUNCTION) 



  #---------------------------
  #   SUB FUNCTION 
  #---------------------------
  def sub(self, sub_name):
    """For use SUB function"""
    return NotIimplemented 

  #---------------------------
  #   DEFSUB FUNCTION 
  #---------------------------
  def defsub(self, sub_name, fct):
    """For use DEFSUB function"""
    return NotIimplemented 

  #---------------------------
  #   LOOP FUNCTION 
  #---------------------------
  def loop(self, nb_loop, fct, *args):
    """for use a realy aerotech loop"""
    AeroCheck.testLoop(nb_loop)
    self.f.write("L," + str(nb_loop) + "\n")
    fct(*args)
    self.f.write("E\n")

  #---------------------------
  #   EOL FUNCTION 
  #---------------------------
  def eol(self, nb=1):  
    """write eol nb times"""
    for i in range(nb):
      self.f.write("\n")
      
  
if __name__ == '__main__' : 
  """some dev tests"""
  M = list()
  for i in range(2):
    M.append( PropFile('test{}.glo'.format(str(i))))

  for i in range(2):  
      rouge = Color(255,0,0)
      M[i].cmt("hello world")
      M[i].cc(Color(100,100,0), cmt="test 1")
      M[i].c(100,100,0, cmt="test 2")
      M[i].r(256, cmt="test 1")
      M[i].g(256, cmt="test 1")
      M[i].b(256, cmt="test 1")
      M[i].d(-256, cmt="test 1")
      M[i].eol()
      M[i].eol()
      M[i].ramp(256,0,0,100, cmt = "test 1")
      M[i].cramp(Color(256,0,0),100, cmt = "test 2")

  def myloop():
    M[1].b(1024, cmt="loop")
    M[1].d(69, cmt="loop")

  M[1].loop(2, myloop)

  M[1].end()
