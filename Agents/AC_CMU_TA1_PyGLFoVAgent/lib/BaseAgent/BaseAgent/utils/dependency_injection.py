# -*- coding: utf-8 -*-
"""
.. module:: utils
   :platform: Linux, Windows, OSX
   :synopsis: A simple DI framework for injecting components into the agent,
              or other components

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>
"""

class DependencyInjection:
   """
   A wrapper class to provide a namespace for DI functionality.  Currently only
   contains static methods, but put in class in case functionality requires
   instancing in the future.

   TODO:  Implement safety checks, and return Nones if unsuccessful
   """

   @staticmethod
   def get_module_and_class(path):
      """
      Helper function to dynamically load modules and classes.

      Arguments
      ---------
      path : string
         Fully qualified class name, in the form module.submodule.ClassName
      """

      # Split the package and class from the qualified path
      module_name = '.'.join(path.split('.')[:-1])
      class_name = path.split('.')[-1]

      # Load the module and get the class
      _module = __import__(module_name, fromlist=[class_name])
      _class = getattr(_module, class_name)

      return _module, _class


   @staticmethod
   def create_instance(path, *args, **kwargs):
      """
      Create an instance of the fully qualified class provided, passing the
      arguments and keyword arguments provided during creation.

      Usage
      -----

      Use case 1:  provide the arguments and keyword arguments directly

         >>> instance1 = DependencyInjection.create_instance('path.to.class.A', 1, 2, arg1=3, arg2=4)

      Use case 2:  provide arguments and keyword arguments as list & dictionary

         >>> arguments = (1,2)
         >>> keyword_arguments = {'arg1':3, 'arg2':4}
         >>> instance2 = DependencyInjection.create_instance('path.to.class.A', *aguments, **keyword_arguments)

      Arguments
      ---------
      path : string
         Fully qualified class name, in the form module.submodule.ClassName
      *args : argument list
         List of positional arguments to pass during instance creation
      **kwargs : keyword argument dictionary
         Dictionary of keyword arguments
      """

      _, _class = DependencyInjection.get_module_and_class(path)

      return _class(*args, **kwargs)


