#!/usr/bin/python

# trying to build my own disassembler

import os
import shutil
import re

#
# Methods
#

def getBinary(_file):
        with open(_file, "rb") as f:
                return str(f.read().encode('bin'))

def getHexStringStreamFromFile(_file):
        with open(_file, "rb") as f:
                return str(f.read().encode('hex'))

def getListFromHexString(_string):
        _list = []
        for i in range(0, len(_string), 2):
                _list.append(_string[i:i+2])
        return _list

def getConstantPoolIntCount(_list):
        _string = "%s%s" % (_list[8],_list[9])
        return int(_string, 16)

def printMagicNumber(_list):
        print "Magic\t\t\t%s%s%s%s" % (_list[0],_list[1],_list[2],_list[3])

def printMinorVersion(_list):
        _hex = _list[4]+_list[5]
        print "Minor\t\t\t%s" % (int(_hex,16))

def printMajorVersion(_list):
        _hex = _list[6]+_list[7]
        print "Major\t\t\t%s" % (int(_hex,16))

def printConstantPoolCount(_list):
        _hex = _list[8]+_list[9]
        print "ConstantPoolCount\t%s" % (int(_hex,16))

def printConstantPool(_list,_constantPoolCount):
                print
                #this skips the known bytes (first ten) at the beginning of the binary .class file
                offset = 10
                #for counter in range(0, _constantPoolCount): 
                for counter in range(1, 38):
                        #print "counter\toffset\thex_found_at_offset"
                        #print "%s\t%s\t%s" % (counter,offset, _list[offset])

                        if _list[offset] == '01':
                                print 'CONSTANT_Utf8_info { '
                                # hack! the number 3 accounts for the tag u1 and the length u2 TODO fix 
                                _01_offset_hack = 3
                                _tag = "%s" % _list[offset]
                                _length = int(_list[offset+1]+_list[offset+2], 16)
                                _bytes = "%s" % (_list[offset+3])

                                print "\tpool_index\thex_offset\tbyte_offset\ttag\tlength\tbytes"
                                print "\t%s\t\t%s\t\t%s\t\t%s\t%s\t%s" % (counter,hex(offset), offset, _tag,  _length, _bytes)
                                print "}"
                                offset = offset + _length + _01_offset_hack

                        elif _list[offset] == '03':
                                print 'CONSTANT_Integer_info {'
                                # hack! the number 3 accounts for the tag u1 and the length u2 TODO fix 
                                _03_offset_hack = 5
                                _tag = "%s" % _list[offset]
                                _bytes = "%s%s%s%s" % (_list[offset+1], _list[offset+2],_list[offset+3],_list[offset+4])
                                _int_value = int(_list[offset+1]+_list[offset+2]+_list[offset+3]+_list[offset+4], 16)
                                print "\tpool_index\thex_offset\tbyte_offset\ttag\tbytes\t\tint_value"
                                print "\t%s\t\t%s\t\t%s\t\t%s\t%s\t%s" % (counter, hex(offset), offset, _tag, _bytes,_int_value)

                                print "}"
                                offset = offset + _03_offset_hack
                        elif _list[offset] == '04':
                                print '04 FOUND'
                                return
                        elif _list[offset] == '05':
                                print '05 FOUND'
                                return
                        elif _list[offset] == '06':
                                print '06 FOUND'
                                return
                        elif _list[offset] == '07':
                                print 'CONSTANT_Class_info {'
                                _07_offset_hack = 3
                                _tag = "%s" % _list[offset]
                                _index = int(_list[offset+2], 16)
                                print "\tpool_index\thex_offset\tbyte_offset\ttag\tname_index\t"
                                print "\t%s\t\t%s\t\t%s\t\t%s\t%s" % (counter,hex(offset),offset, _tag, _index)
                                print '}'
                                offset = offset + _07_offset_hack

                        elif _list[offset] == '08':
                                print 'CONSTANT_String_info {'
                                _08_offset_hack = 3
                                _tag = "%s" % _list[offset]
                                _string_index = "%s%s" % (_list[offset+1], _list[offset+2])

                                print "\tpool_index\thex_offset\tbyte_offset\ttag\tstring_index"
                                print "\t%s\t\t%s\t\t%s\t\t%s\t%s" % (counter,hex(offset),offset, _tag, _string_index)
                                print '}'
                                offset = offset + _08_offset_hack
                        elif _list[offset] == '09':
                                print 'CONSTANT_Fieldref_info {'
                                _09_offset_hack = 5
                                _tag = "%s" % _list[offset]
                                _class_index = "%s%s" % (_list[offset+1], _list[offset+2])
                                _name_and_type_index = "%s%s" % (_list[offset+3],_list[offset+4])

                                print "\tpool_index\thex_offset\tbyte_offset\ttag\tclass_index\tname_and_type_index"
                                print "\t%s\t\t%s\t\t%s\t\t%s\t%s\t\t%s" % (counter, hex(offset), offset, _tag, _class_index, _name_and_type_index)
                                print '}'
                                offset = offset + _09_offset_hack
                        elif _list[offset] == '0a':
                                print 'CONSTANT_Methodref_info { '
                                _0a_offset_hack = 5
                                _tag = "%s" % _list[offset]
                                _class_index = "%s%s" % (_list[offset+1], _list[offset+2])
                                _name_and_type_index = "%s%s" % (_list[offset+3],_list[offset+4])

                                print "\tpool_index\thex_offset\tbyte_offset\ttag\tclass_index\tname_and_type_index"
                                print "\t%s\t\t%s\t\t%s\t\t%s\t%s\t\t%s" % (counter, hex(offset), offset, _tag, _class_index, _name_and_type_index)
                                print '}'
                                offset = offset + _0a_offset_hack
                        elif _list[offset] == '0b':
                                print '11/hex 0b FOUND'
                                return
                        elif _list[offset] == '0c':
                                print 'CONSTANT_NameAndType_info {'
                                # hack! the number 3 accounts for the tag u1 and the length u2 TODO fix 
                                _0c_offset_hack = 5
                                _tag = "%s" % _list[offset]
                                _name_index = "%s%s" % (_list[offset+1], _list[offset+2])
                                _descriptor_index = "%s%s" % (_list[offset+3],_list[offset+4])

                                print "\tpool_index\thex_offset\tbyte_offset\ttag\tname_index\tdescriptor_index"
                                print "\t%s\t\t%s\t\t%s\t\t%s\t%s\t\t%s" % (counter, hex(offset), offset, _tag, _name_index, _descriptor_index)
                                print '}'
                                offset = offset + _0c_offset_hack
                        elif _list[offset] == '0f':
                                print '15/hex 0c FOUND'
                                return
                        elif _list[offset] == '10':
                                print '16/hex 10 FOUND'
                                return
                        elif _list[offset] == '12':
                                print '18/hex 12 FOUND'
                                return


classFile = 'Code.class'
hexString = getHexStringStreamFromFile(classFile)
bytecodeList = getListFromHexString(hexString)

printMagicNumber(bytecodeList)
printMinorVersion(bytecodeList)
printMajorVersion(bytecodeList)
printConstantPoolCount(bytecodeList)
printConstantPool(bytecodeList,getConstantPoolIntCount(bytecodeList))
