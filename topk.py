import utils

class ZHeap:
    def __init__(self, item=[], id=[]):
        self.items = item
        self.ids = id
        self.heapsize = len(self.items)

    def _getLeftChild(self, i):
        return 2 * i + 1

    def _getRightChild(self, i):
        return 2 * i + 2

    def _getParent(self, i):
        return int((i - 1) / 2)

    def _percolate(self, i):
        # 最小堆化：使以i为根的子树成为最小堆
        l = self._getLeftChild(i)
        r = self._getRightChild(i)
        if l < self.heapsize and self.items[l] < self.items[i]:
            smallest = l
        else:
            smallest = i

        if r < self.heapsize and self.items[r] < self.items[smallest]:
            smallest = r

        if smallest != i:
            self.items[i], self.items[smallest] = self.items[smallest], self.items[i]
            self.ids[i], self.ids[smallest] = self.ids[smallest], self.ids[i]
            self._percolate(smallest)

    def _insert(self, val, id):
        # 插入一个值val，并且调整使满足堆结构
        self.items.append(val)
        self.ids.append(id)
        idx = len(self.items) - 1
        parIdx = int(self._getParent(idx))
        while parIdx >= 0:
            if self.items[parIdx] > self.items[idx]:
                self.items[parIdx], self.items[idx] = self.items[idx], self.items[parIdx]
                self.ids[parIdx], self.ids[idx] = self.ids[idx], self.ids[parIdx]
                idx = parIdx
                parIdx = self._getParent(parIdx)
            else:
                break
        self.heapsize += 1

    def _delete(self):
        # 删除最后一个值，调整使满足堆结构
        last = len(self.items) - 1
        if last < 0:
            # 堆为空
            return None
        # else:
        self.items[0], self.items[last] = self.items[last], self.items[0]
        self.ids[0], self.ids[last] = self.ids[last], self.ids[0]
        val = self.items.pop()
        id = self.ids.pop()
        self.heapsize -= 1
        self._percolate(0)
        return id


    def minHeap(self):
        # 建立最小堆, O(nlog(n))
        i = self._getParent(len(self.items) - 1)
        while i >= 0:
            self._percolate(i)
            i -= 1

    def _show(self):
        print(self.items)


class ZPriorityQ(ZHeap):
    def __init__(self, item=[]):
        ZHeap.__init__(self, item)

    def enQ(self, val, id):
        ZHeap._insert(self, val, id)

    def deQ(self):
        val = ZHeap._delete(self)
        return val

VSM = utils.get_from_file('VSM')
Wordlist = utils.get_from_file('wordlist')

def cosinescore(Qlist, docID):
	# print(docID)
	global VSM
	global Wordlist

	doc_magnitude_0 = VSM[str(docID)]
	doc_magnitude_1 = []
	for score in doc_magnitude_0:
		if not score.isdigit():
			doc_magnitude_1.append(score)
		else:
			for i in range(int(score)):
				doc_magnitude_1.append('0.0')
	if len(doc_magnitude_1) < len(Wordlist):
		num = len(Wordlist) - len(doc_magnitude_1)
		# append_list = []
		doc_magnitude_1.extend(['0.0'] * num)

	result = 0
	for Qword in Qlist:
		if Qword != "AND" and Qword != "OR" and Qword != "NOT":
			index = Wordlist.index(Qword)
			# print(index)
			# print(len(doc_magnitude_1))
			result += float(doc_magnitude_1[index])
	# c_score = '%.20f' % float(result)
	# print(result)
	return result



def topK(wordlist, docID):

    K = int(input("显示排序前多少名的文档？\n输入-1显示全部\n"))
    print("\n\n************* 查询结果 ************\n\n共找到 ",len(docID), " 篇文档\n")
    pq = ZPriorityQ()
    if len(docID) < K or K == -1:
        K = len(docID)

    for doc in docID:
        #calculate the score of cos(q,d)
        value = cosinescore(wordlist, doc)

        doc_score = - float(value)
        pq.enQ(doc_score, doc)
    result = []
    for i in range(K):
        doc = pq.deQ()
        # print(score_t)
        result.append(doc)
    # result.reverse()
    print("显示前", len(result), " 篇文档\n")
    print(result)
    stop = input("\n按Y查看文档，任意键跳过查看...\n")
    if(stop == 'Y' or stop == 'y'):
        return result
    else:
        return []
