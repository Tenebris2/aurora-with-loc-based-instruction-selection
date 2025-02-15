import re
from pprint import pprint
from enum import Enum

FILE_TO_WRITE = "decompiled_code"
OFFSET = "00"
GLOBAL_END_INDICATOR = "END_OF_LINE"
JUMP_FILE = "jump_instructions"
START_ADDRESS = "00101000"
END_ADDRESS = "0010136c"
MID_ADDRESS_FILE = "mid_addresses"
jump_set = set()
address_set = set()

INS = []


class SelectionMethod:
    BEGIN = 1
    MIDDLE = 2
    END = 3


def extract_number(s):
    if not isinstance(s, str):
        s = s.toString()
    match = re.match(r"(\d+):", s)
    return int(match.group(1)) if match else float("inf")


def extract_hex_address(s):
    match = re.match(r"(.*?):", s)
    return match.group(1) if match else ""


def getLines(markup):
    line_set = set()

    for t in markup.tokenIterator(True):
        line_set.add(t.getLineParent())
    line_set = {x for x in line_set if x is not None}

    return line_set


def extract_addr(line):
    token_set = line.getAllTokens()
    addr_set = set()

    for token in token_set:
        addr_set.add(token.getMinAddress())
        addr_set.add(token.getMaxAddress())

    return sorted({x for x in addr_set if x is not None})


def disassembleInstructions(
    Disassembler, AddressSet, program, flat_api, startAddr, endAddr
):

    address_set = AddressSet(startAddr, endAddr)

    for address in address_set.getAddresses(True):
        flat_api.disassemble(address)


def getExecutableSectionFunctions(program, flat_api):

    function_manager = program.getFunctionManager()
    functions = function_manager.getFunctions(True)

    block = flat_api.getMemoryBlock(".text")
    section_functions = []
    for f in functions:
        entry_point = f.getEntryPoint()
        if block.contains(entry_point):
            section_functions.append(f)
    return section_functions


def getInsts(addrs, AddressSet, flat_api):
    if len(addrs) > 1:
        addr_set = AddressSet(addrs[0], addrs[len(addrs) - 1])
    else:
        addr_set = AddressSet(addrs[0])
    insts = []
    # test
    tmp_inst = []
    #
    for addr in addr_set.iterator(True):
        for a in addr:
            if flat_api.getInstructionAt(a) != None:
                inst = (
                    "\t"
                    + a.toString()
                    + ":"
                    + flat_api.getInstructionAt(a).toString()
                    + "\n"
                )
                # test
                tmp_inst.append(a)
                if flat_api.getInstructionAt(a).getFlowType().isJump():
                    address_set.add(flat_api.getInstructionAt(a).getAddress())
                    jump_set.add(flat_api.getInstructionAt(a).getAddress())
                #
                insts.append(inst)
    if len(insts) >= 1:
        address_set.add(tmp_inst[len(tmp_inst) - 1])
        insts.append(GLOBAL_END_INDICATOR + "\n")
    INS.append(tmp_inst)
    return insts


def extractLastLineInstruction():
    instruction_addr = set()
    with open(FILE_TO_WRITE, "r") as f:
        lines = f.readlines()
        for line_no, line in enumerate(lines, 1):
            current_line = "".join(line).strip()
            next_line = (
                "".join(lines[line_no]).strip()
                if line_no < len(lines)
                else "No next line"
            )
            if "line of code" in next_line and OFFSET in current_line:
                instruction_addr.add(extract_hex_address(current_line))

    return instruction_addr


def writeInstructionMappingToFile(function_name, markup, flat_api, AddressSet):
    lines = getLines(markup)
    lines = sorted(lines, key=lambda s: extract_number(s))

    write_data = []
    write_data.append(f"\n\n\nFunction: {function_name}\n")
    for line in lines:
        if extract_addr((line)):
            write_data.append("----------------------------------------------\n")
            write_data.append(line.toString() + "\n")
            write_data.append(getInsts(extract_addr(line), AddressSet, flat_api))

    with open(FILE_TO_WRITE, "a") as file:
        for line in write_data:
            file.write("".join(line))


# test


def extractJumpSet():
    temp = jump_set
    with open(JUMP_FILE, "w") as file:
        for t in temp:
            file.write(t.toString() + "\n")


def definedUndefinedFunctions(
    currentProgram, monitor, flat_api, AddressSet, IsolatedEntrySubModel
):
    set = AddressSet()
    listing = currentProgram.getListing()

    initer = listing.getInstructions(currentProgram.getMemory(), True)
    while initer.hasNext() and not monitor.isCancelled():
        instruct = initer.next()
        set.addRange(instruct.getMinAddress(), instruct.getMaxAddress())

    iter = listing.getFunctions(True)
    while iter.hasNext() and not monitor.isCancelled():
        f = iter.next()
        set.delete(f.getBody())

    if set.getNumAddressRanges() == 0:
        pass

    # go through address set and find the actual start of flow into the dead code
    submodel = IsolatedEntrySubModel(currentProgram)
    subIter = submodel.getCodeBlocksContaining(set, monitor)
    codeStarts = AddressSet()
    while subIter.hasNext():
        block = subIter.next()
        deadStart = block.getFirstStartAddress()
        codeStarts.add(deadStart)

    for startAdr in codeStarts:
        phyAdr = startAdr.getMinAddress()
        print("Undef Func detected at: " + phyAdr.toString())
        flat_api.createFunction(phyAdr, None)


def writeIns(selection_method):
    current_ins = INS

    middle_ins = set()
    for i in current_ins:
        if len(i) >= 1:
            if selection_method == SelectionMethod.BEGIN:
                middle_ins.add(i[0])
            elif selection_method == SelectionMethod.MIDDLE:
                middle_ins.add(i[len(i) // 2])
            elif selection_method == SelectionMethod.END:
                middle_ins.add(i[len(i) - 1])
        else:
            continue

    with open(MID_ADDRESS_FILE, "w") as file:
        for ins in middle_ins:
            file.write(ins.toString() + "\n")
