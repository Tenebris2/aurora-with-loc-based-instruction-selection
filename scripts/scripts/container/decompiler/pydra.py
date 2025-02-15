import os
import pyhidra
import re
import sys
import lib

JUMP_FILE = "jump_instructions"
INSTRUCTION_FILE = "instructions"
TARGET = sys.argv[1]
pyhidra.start()
print("Starting..")
with pyhidra.open_program(TARGET, analyze=True) as flat_api:
    program = flat_api.getCurrentProgram()
    listing = program.getListing()
    monitor = flat_api.getMonitor()

    from ghidra.util.task import ConsoleTaskMonitor
    from ghidra.app.decompiler import DecompInterface, DecompileOptions
    from ghidra.program.model.address import AddressSet
    from ghidra.program.disassemble import Disassembler
    from ghidra.program.model.address import Address
    from ghidra.program.model.block import IsolatedEntrySubModel

    decomp_interface = DecompInterface()
    options = DecompileOptions()
    decomp_interface.setOptions(options)
    decomp_interface.openProgram(flat_api.getCurrentProgram())

    mb = flat_api.getMemoryBlock(".text")

    function_manager = program.getFunctionManager()
    functions = function_manager.getFunctions(True)
    address_factory = program.getAddressFactory()

    program.setImageBase(address_factory.getAddress("0"), True)

    with open(JUMP_FILE, "w") as file:
        file.write("")

    startAddr = mb.getStart()

    endAddr = mb.getEnd()
    # lib.disassembleInstructions(Disassembler, AddressSet, program, flat_api, startAddr, endAddr)
    #
    instruction = listing.getInstructionAt(startAddr)

    lib.definedUndefinedFunctions(
        program, monitor, flat_api, AddressSet, IsolatedEntrySubModel
    )
    with open(JUMP_FILE, "a") as file:
        while instruction != None and mb.contains(instruction.getAddress()):
            if instruction.getMnemonicString().startswith("J"):
                file.write(instruction.getAddress().toString() + "\n")
            instruction = instruction.getNext()

    internal_functions = functions

    with open(lib.FILE_TO_WRITE, "w") as file:
        file.write("")

    with open(INSTRUCTION_FILE, "w") as file:
        file.write("")
    for f in internal_functions:
        function_name = f.getName()
        print(function_name)
        res = decomp_interface.decompileFunction(f, 60, ConsoleTaskMonitor())
        decompiled_function = res.getDecompiledFunction()
        markup = res.getCCodeMarkup()

        if markup is not None:
            lib.writeInstructionMappingToFile(
                function_name, markup, flat_api, AddressSet
            )

lines_to_write = lib.extractLastLineInstruction()

with open(INSTRUCTION_FILE, "a") as file:
    for line in lines_to_write:
        file.write(line + "\n")

lib.extractJumpSet()
lib.writeIns(lib.SelectionMethod.BEGIN)
