import score
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

def topK(wordlist, docID):

    K = int(input("显示排序前多少的文档？\n输入-1显示全部\n"))
    print("\n\n************* 查询结果 ************\n\n共找到 ",len(docID), " 篇文档\n")
    VSM_sum = utils.get_from_file('VSM_sum')
    pq = ZPriorityQ()
    if len(docID) < K or K == -1:
        K = len(docID)
    for doc in docID:
        #calculate the score of cos(q,d)
        #value = score.cosinescore(wordlist, doc)
        #print(value)
        #get the tf-idf
        #doc_score = VSM_sum[str(doc)]+value
        if str(doc) in VSM_sum:
            doc_score = VSM_sum[str(doc)]
        pq.enQ(doc_score, doc)
    result = []
    for i in range(K):
        doc = pq.deQ()
        #print(doc)
        result.append(doc)
    print("显示前", len(result), " 篇文档\n")
    print(result)
    stop = input("\n按任意键查看文档...\n")
    return result
