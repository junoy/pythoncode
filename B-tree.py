#B tree
class TreeNode:
    def __init__(self,x):
        self.val=x
        self.left=None
        self.right=None
 
def builtTree():
    root=None
    val=input("Enter the value:")
    if(val=='#'):
        pass
    else:
        root=TreeNode(val)
        root.left=builtTree()
        root.right=builtTree()
    return root
 
def PreTraver(root):
    if root==None:
        return
    else:
        print(root.val,end=" ")
    traver(root.left)
    traver(root.right)
 
def MidTraver(root):
    if root==None:
        return
    MidTraver(root.left)
    print(root.val,end=" ")
    MidTraver(root.right)
 
def ReTraver(root):
    if root==None:
        return
    ReTraver(root.left)
    ReTraver(root.right)
    print(root.val,end=" ")
 
def deepth(root):
    if root==None:
        return 1
    leftDeepth=deepth(root.left)+1
    rightDeepth=deepth(root.right)+1
    if leftDeepth>rightDeepth:
        return leftDeepth
    else:
        return rightDeepth
 
def main():
    root=builtTree()
    if(root==None):
        print("builtTree failed")
 
 
if __name__=='__main__':
    main()
else:
    print("test.py has worked")