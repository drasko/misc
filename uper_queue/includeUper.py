import struct, time, types, os

class UPER:       
    def stop(self):
        for i in range(7):
            self.detachInterrupt(i)
        self.reader.stop()
        self.ser.close()

    def encodeINT(self, intarg):
        if intarg < 64:
            return(chr(intarg))
        packedint = struct.pack( '>I', intarg ).lstrip('\x00')
        return(chr(0xc0 | (len(packedint) -1)) + packedint)

    def encodeBYTES(self, bytestr):
        if len( bytestr ) < 64:
            return (chr(0x40 | len(packedint)) + bytestr)
        packedlen = struct.pack( '>I', len(bytestr)).lstrip('\x00')
        if len(packedlen) == 1:
            return('\xc4'+packedlen+bytestr)
        elif len(pakedlen) == 2:
            return('\xc5' + packedlen + bytestr)
        else:
            print "UPER API: error - too long string"

    def encodeSFP(self, command, args):
        functions = { types.StringType : self.encodeBYTES, types.IntType : self.encodeINT }
        SFPcommand = chr(command) + ''.join(functions[ type(arg) ]( arg ) for arg in args)
        SFPcommand = '\xd4' + struct.pack('>H', len(SFPcommand)) + SFPcommand
        return(SFPcommand)

    def decodeSFP(self, buffer):
        result = []
        if buffer[0:1] != '\xd4':
            return( result )
        buflen = struct.unpack('>H', buffer[1:3])[0] + 3
        result.append( struct.unpack('b', buffer[3:4])[0] )
        pointer = 4
        args = []
        while pointer < buflen:
            argtype = ord(buffer[pointer:pointer+1])
            pointer +=1
            if argtype < 64:                    #short int
                args.append(argtype)
            elif argtype < 128:                    #short str
                arglen = argtype & 0x3f
                args.append(buffer[pointer:pointer+arglen])
                pointer += arglen
            else:
                arglen = argtype & 0x0f            #decoding integers
                if arglen == 0:
                    args.append(ord(buffer[pointer:pointer+1]))
                elif arglen == 1:
                    args.append(struct.unpack('>H', buffer[pointer:pointer+2])[0])
                elif arglen == 2:
                    args.append(struct.unpack('>I', '\x00' + buffer[pointer:pointer+3])[0])
                elif arglen == 3:
                    args.append(struct.unpack('>I', buffer[pointer:pointer+4])[0])
                pointer += arglen + 1

                if arglen == 4:
                    arglen = ord(buffer[pointer:pointer+1])
                    pointer += 1
                    args.append(buffer[pointer:pointer+arglen])
                    pointer += arglen
                elif arglen == 5:
                    arglen = struct.unpack('>H', buffer[pointer:pointer+2])[0]
                    pointer += 2
                    args.append(buffer[pointer:pointer+arglen])
                    pointer += arglen
        result.append(args)
        return(result)

    def UPER_IO(self, ret, buf):
        with self.sem:
            # Put command to qin
            self.qin.put(buf)
            if ret == 0:
                return
            data = self.qout.get()

        return(data)

    def setPrimary(self, pinID):
        self.UPER_IO(0, self.encodeSFP(1, [pinID]))

    def setSecondary(self, pinID):
        self.UPER_IO(0, self.encodeSFP(2, [pinID]))

    def pinMode(self, pinID, pinMode):
        self.UPER_IO(0, self.encodeSFP(3, [pinID, pinMode]))

    def digitalWrite(self, pinID, value):
        self.UPER_IO(0, self.encodeSFP(4, [pinID, value]))

    def digitalRead(self, pinID):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP( 5, [pinID])))[1][1])

    def attachInterrupt(self, interruptID, pinID, mode):
        self.UPER_IO(0, self.encodeSFP(6, [interruptID, pinID, mode])) 

    def detachInterrupt(self, interruptID):
        self.UPER_IO(0, self.encodeSFP(7, [interruptID])) 

    def analogRead(self, analogPinID):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP(10, [analogPinID])))[1][1])

    def pwm0_begin(self, period):
        #print "pwm0_begin period:", period
        self.UPER_IO(0, self.encodeSFP(50, [period]))     

    def pwm1_begin(self, period):
        #print "pwm1_begin period:", period
        self.UPER_IO(0, self.encodeSFP(60, [period])) 

    def pwm0_set(self, channel, high_time):
        #print "pwm0_set high_time:", high_time
        self.UPER_IO(0, self.encodeSFP(51, [channel, high_time]))

    def pwm1_set(self, channel, high_time):
        #print "pwm1_set high_time:", high_time
        self.UPER_IO(0, self.encodeSFP(61, [channel, high_time]))

    def pwm0_end(self):
        self.UPER_IO(0, self.encodeSFP(52, []))

    def pwm1_end(self):
        self.UPER_IO(0, self.encodeSFP(62, []))

    def spi0_begin(self, divider, mode):
        self.UPER_IO(0, self.encodeSFP(20, [divider, mode]))

    def spi0_trans(self, data, respond):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP(21, [data, respond])))[1][0])

    def spi0_end(self):
        self.UPER_IO(0, self.encodeSFP( 22, []))
         
    def i2c_begin(self):
        self.UPER_IO(0, self.encodeSFP(40, []))

    def i2c_trans(self, address, writeData, readLength):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP(41, [address, writeData, readLength]))))

    def i2c_end(self):
        self.UPER_IO(0, self.encodeSFP( 42, []))

    def registerWrite(self, registerAddress, value):
        self.UPER_IO(0, self.encodeSFP(100, [registerAddress, value]))

    def registerRead(self, registerAddress):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP(101, [registerAddress])))[1][1])

    def getDeviceInfo(self):
        device_info = []
        result = self.decodeSFP(self.UPER_IO(1, self.encodeSFP(255, [])))
        if result[0] != -1:
            print "UPER error: getDeviceInfo wrong code."
            return
        result = result[1]
        if result[0] >> 24 != 0x55: # 0x55 == 'U'
            print "UPER error, getDeviceInfo unknown device/firmware type"
            return
        device_info.append("UPER") # type
        device_info.append((result[0] & 0x00ff0000) >> 16) #fw major
        device_info.append(result[0] & 0x0000ffff) #fw minor
        device_info.append(result[1]) # 16 bytes long unique ID from UPER CPU
        device_info.append(result[2]) # UPER LPC CPU part number
        device_info.append(result[3]) # UPER LPC CPU bootload code version
        return(device_info)

    def internalCallBack(intdata):
        #print"default CallBack is working %r" % intdata
        return

    def __init__(self, qin, qout, sem):
        self.qin = qin
        self.qout = qout
        self.sem = sem
