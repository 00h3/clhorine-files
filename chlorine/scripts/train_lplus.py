from chlorine.lplus.train import train
import argparse
p=argparse.ArgumentParser()
p.add_argument("--data",default="data/lplus_corpus.txt")
p.add_argument("--out",default="checkpoints/lplus.pt")
p.add_argument("--steps",type=int,default=2000)
a=p.parse_args()
train(a.data,a.out,a.steps)
