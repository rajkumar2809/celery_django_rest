
class TestDat():
#     def __init__(self):
#         self.Dat1 = None
#         self.Dat2 = None
    def __init__(self):
        self.s_name = None
        self.s_id = None
        self.d_name = None
        self.s_count = None

TestArray = [] #empty array
size = 2       #number of loops

for x in range(size):  # appending empty objects
    TestArray.append(TestDat())

#initialize later
TestArray[0].s_name = 0
TestArray[0].s_id = 1
TestArray[0].d_name = 2
TestArray[0].s_count = 12

TestArray[1].s_name = 21
TestArray[1].s_id = 12
TestArray[1].d_name = 32
TestArray[1].s_count = 412

print("print everithing")
for x in range(len(TestArray)):
    print("object "+str(x))
    print(TestArray[x].s_name)
    print(TestArray[x].s_id)
    print(TestArray[x].d_name)
    print(TestArray[x].s_count)
    # print(TestArray[x].Dat2)
