# -*- coding: utf-8 -*-
"""
Factory.py

Metaclass Based Class Factory Example

Works with Python 2.7

@author: Aifeng Yun
@date: 4/21/2016

    This example demonstrates the suggested use of the metaclass technique  
    for dynamically creating classes based on the metaclass.

    Change Log:

        4/21/2016 - Added example demonstrating the overriding of the 
                    __init__ function on the dynamically generated factory 
                    product classes.

        3/20/2016 - Initial release.

"""

from pprint import pprint
from types import DictType

class FactoryMeta(type):
    """ Factory Metaclass """

    # @ Anything "static" (bounded to the classes rather than the instances) 
    #   goes in here. Or use "@classmethod" decorator to bound it to meta. 
    # @ Note that these members won't be visible to instances, you have to 
    #   manually add them to the instances in metaclass' __call__ if you wish
    #   to access them through a instance directly (see below).
    extra = "default extra"
    count = 0

    def clsVar(cls):
        print "Class member 'var': " + str(cls.var)

    @classmethod
    def metaVar(meta):
        print "Metaclass member 'var': " + str(meta.var)

    def __new__(meta, name, bases, dict):
        # @ Metaclass' __new__ serves as a bi-functional slot capable for
        #   initiating the classes as well as alternating the meta.
        # @ Suggestion is putting majority of the class initialization code
        #   in __init__, as you can directly reference to cls there; saving 
        #   here for anything you want to dynamically added to the meta (such 
        #   as shared variables or lazily GC'd temps).
        # @ Any changes here to dict will be visible to the new class and their 
        #   future instances, but won't affect the metaclass. While changes 
        #   directly through meta will be visible to all (unless you override 
        #   it later).
        dict['new_elem'] = "effective"
        meta.var = "Change made to %s by metaclass' __new__" % str(meta)
        meta.count += 1
        print "================================================================"
        print " Metaclass's __new__ (creates class objects)"
        print "----------------------------------------------------------------"
        print "Bounded to object: " + str(meta)
        print "Bounded object's __dict__: "
        pprint(DictType(meta.__dict__), depth = 1)
        print "----------------------------------------------------------------"
        print "Parameter 'name': " + str(name)
        print "Parameter 'bases': " + str(bases)
        print "Parameter 'dict': "
        pprint(dict, depth = 1)
        print "\n"
        return super(FactoryMeta, meta).__new__(meta, name, bases, dict)

    def __init__(cls, name, bases, dict):
        # @ Metaclass' __init__ is the standard slot for class initialization.
        #   Classes' common variables should mainly goes in here.
        # @ Any changes here to dict won't actually affect anything. While 
        #   changes directly through cls will be visible to the created class 
        #   and its future instances. Metaclass remains untouched.
        dict['init_elem'] = "defective"
        cls.var = "Change made to %s by metaclass' __init__" % str(cls)
        print "================================================================"
        print " Metaclass's __init__ (initiates class objects)"
        print "----------------------------------------------------------------"
        print "Bounded to object: " + str(cls)
        print "Bounded object's __dict__: "
        pprint(DictType(cls.__dict__), depth = 1)
        print "----------------------------------------------------------------"
        print "Parameter 'name': " + str(name)
        print "Parameter 'bases': " + str(bases)
        print "Parameter 'dict': "
        pprint(dict, depth = 1)
        print "\n"
        return super(FactoryMeta, cls).__init__(name, bases, dict)

    def __call__(cls, *args):
        # @ Metaclass' __call__ gets called when a class name is used as a 
        #   callable function to create an instance. It is called before the 
        #   class' __new__.
        # @ Instance's initialization code can be put in here, although it 
        #   is bounded to "cls" rather than instance's "self". This provides 
        #   a slot similar to the class' __new__, where cls' members can be 
        #   altered and get copied to the instances.
        # @ Any changes here through cls will be visible to the class and its 
        #   instances. Metaclass remains unchanged.
        cls.var = "Change made to %s by metaclass' __call__" % str(cls)
        # @ "Static" methods defined in the meta which cannot be seen through 
        #   instances by default can be manually assigned with an access point 
        #   here. This is a way to create shared methods between different 
        #   instances of the same metaclass.
        cls.metaVar = FactoryMeta.metaVar
        print "================================================================"
        print " Metaclass's __call__ (initiates instance objects)"
        print "----------------------------------------------------------------"
        print "Bounded to object: " + str(cls)
        print "Bounded object's __dict__: "
        pprint(DictType(cls.__dict__), depth = 1)
        print "\n"
        return super(FactoryMeta, cls).__call__(*args)

class Factory(object):
    """ Factory Class """

    # @ Anything declared here goes into the "dict" argument in the metaclass'  
    #   __new__ and __init__ methods. This provides a chance to pre-set the 
    #   member variables desired by the two methods, before they get run. 
    # @ This also overrides the default values declared in the meta. 
    __metaclass__ = FactoryMeta
    extra = "overridng extra"

    def selfVar(self):
        print "Instance member 'var': " + str(self.var)

    @classmethod
    def classFactory(cls, name, bases, dict):
        # @ With a factory method embedded, the Factory class can act like a 
        #   "class incubator" for generating other new classes.
        # @ The dict parameter here will later be passed to the metaclass' 
        #   __new__ and __init__, so it is the right place for setting up 
        #   member variables desired by these two methods.
        dict['class_id'] = cls.__metaclass__.count  # An ID starts from 0.
        # @ Note that this dict is for the *factory product classes*. Using 
        #   metaclass as callable is another way of writing class definition, 
        #   with the flexibility of employing dynamically generated members 
        #   in this dict.
        # @ Class' member methods can be added dynamically by using the exec 
        #   keyword on dict.
        exec(cls.extra, dict)
        exec(dict['another_func'], dict)
        exec(dict['init_func'], dict)
        return cls.__metaclass__(name + ("_%02d" % dict['class_id']), bases, dict)

    def __new__(cls, function):
        # @ Class' __new__ "creates" the instances.
        # @ This won't affect the metaclass. But it does alter the class' member
        #   as it is bounded to cls.
        cls.extra = function
        print "================================================================"
        print " Class' __new__ (\"creates\" instance objects)"
        print "----------------------------------------------------------------"
        print "Bounded to object: " + str(cls)
        print "Bounded object's __dict__: "
        pprint(DictType(cls.__dict__), depth = 1)
        print "----------------------------------------------------------------"
        print "Parameter 'function': \n" + str(function)
        print "\n"
        return super(Factory, cls).__new__(cls)

    def __init__(self, function, *args, **kwargs):
        # @ Class' __init__ initializes the instances.
        # @ Changes through self here (normally) won't affect the class or the 
        #   metaclass; they are only visible locally to the instances.
        # @ However, here you have another chance to make "static" things 
        #   visible to the instances, "locally".
        self.classFactory = self.__class__.classFactory
        print "================================================================"
        print " Class' __init__ (initiates instance objects)"
        print "----------------------------------------------------------------"
        print "Bounded to object: " + str(self)
        print "Bounded object's __dict__: "
        pprint(DictType(self.__dict__), depth = 1)
        print "----------------------------------------------------------------"
        print "Parameter 'function': \n" + str(function)
        print "\n"
        return super(Factory, self).__init__(*args, **kwargs)
# @ The metaclass' __new__ and __init__ will be run at this point, where the 
#   (manual) class definition hitting its end.
# @ Note that if you have already defined everything well in a metaclass, the
#   class definition can go dummy with simply a class name and a "pass".
# @ Moreover, if you use class factories extensively, your only use of a 
#   manually defined class would be to define the incubator class.

"""================================================================================================================================"""
""" Test Cases """

func1 = (
    "def printElems(self):\n"
    "   print \"Member new_elem: \" + self.new_elem\n"
    "   print \"Member init_elem: \" + self.init_elem\n"
    )
factory = Factory(func1)

factory.clsVar()    # Will raise exception
Factory.clsVar()
factory.metaVar()
factory.selfVar()

func2 = (
    "@classmethod\n"
    "def printClassID(cls):\n"
    "   print \"Class ID: %02d\" % cls.class_id\n"
    )
func3 = (
    "def __init__(self, *args, **kwargs):\n"
    "   print \"Product Class' __init__ is getting called...\"\n"
    "   return super(self.__class__, self).__init__(*args, **kwargs)\n"
    )
ProductClass1 = factory.classFactory("ProductClass", (object, ), { 'another_func': func2, 'init_func': func3 })

product = ProductClass1()
product.printClassID()
product.printElems()    # Will raise exception

ProductClass2 = Factory.classFactory("ProductClass", (Factory, ), { 'another_func': "pass" })
ProductClass2.printClassID()    # Will raise exception
ProductClass3 = ProductClass2.classFactory("ProductClass", (object, ), { 'another_func': func2 })
