import xlsxwriter
from datetime import date

# dictionary, might use
recordTypes_dict = {"supplier": 1, "address": 2, "item": 3, "quantity": 4}


class Remito:

    ##INIT
    def __init__(self, path):
        # file location
        self.path = path
        self.__setCells__()

        self.workbook = xlsxwriter.Workbook(path)

    # Set starting cell positions for writing
    def __setCells__(self):
        self.nameColumn = 2
        self.nameRow = 2
        self.addressColumn = 2
        self.addressRow = 3
        self.itemCol = 2
        self.itemRow = 5
        self.qtyCol = 4
        self.qtyRow = 5

    def addWorksheet(self, name):
        self.worksheet = self.workbook.add_worksheet(name)
        self.__setCells__()

    # This will write on the "current" worksheet.
    def write(self, recordType, line):
        if recordType == 1:
            r = self.nameRow
            c = self.nameColumn
        elif recordType == 2:
            r = self.addressRow
            c = self.addressColumn
        elif recordType == 3:
            r = self.itemRow
            c = self.itemCol
            self.itemRow += 1
        elif recordType == 4:
            r = self.qtyRow
            c = self.qtyCol
            # increments row to add items
            self.qtyRow += 1

        self.worksheet.write(r, c, line)

    def close(self):
        self.workbook.close()


with open("proveedores.txt", "r") as reader:

    print("starting")
    remito = Remito("diaDeHoy.xlsx")

    processingSupplier = 1
    # We assume the first row is valid
    # when there is a blank row, we assume current supplier ended and we need to re-start the structure

    # structure:
    # 1- provider name
    # 2- address
    # 3...N - item, quantity

    # start with suppliers
    # if processingSupplier == 1:

    line = reader.readline()
    while line != "":
        if line == "\n":
            # blank lines indicates previous supplier ended. Get the next line
            processingSupplier = 1
            line = reader.readline()
        if processingSupplier == 1:
            remito.addWorksheet(line)
            remito.write(recordTypes_dict["supplier"], line)
            # get next line: address
            line = reader.readline()
            remito.write(recordTypes_dict["address"], line)
            processingSupplier += 1
            # get next line, should be an item
            line = reader.readline()
        if processingSupplier > 1:
            # process items
            if line != "":
                splitLine = line.split(",")
                remito.write(recordTypes_dict["item"], splitLine[0])
                remito.write(recordTypes_dict["quantity"], splitLine[1])
        line = reader.readline()

    remito.close()
