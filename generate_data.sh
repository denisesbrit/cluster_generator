# setup:
delta=1
length=100
height=100

# constants:
repetitions=5
numentities=50
numpoints=100
clusterdist=6


if false; then
for seed in $(seq 1 $repetitions)
do
	for i in $(seq 0 127)
	do
		if ((1 & i)); then
			numclusters=10
		else
			numclusters=2
		fi
		
		if ((1 << 1 & i)); then
			numclouds=5
		else
			numclouds=2
		fi
		
		if ((1 << 2 & i)); then
			noise=0.3
		else
			noise=0
		fi			

		if ((1 << 3 & i)); then
			clusterbalan=0.7
		else
			clusterbalan=$(python -c 'import sys; print 1.0 / float(sys.argv[1])' "$numclusters")
		fi	
		
		if ((1 << 4 & i)); then
			cloudbalan=0.7
		else
			cloudbalan=$(python -c 'import sys; print 1.0 / float(sys.argv[1])' "$numclouds")
		fi	

		echo "python synthetic_generator.py $numclusters $numclouds $noise $clusterbalan $cloudbalan $clusterdist $seed $numentities $numpoints $delta $length $height tests/teste_"${i}"_"${seed}""
		python synthetic_generator.py $numclusters $numclouds $noise $clusterbalan $cloudbalan $clusterdist $seed $numentities $numpoints $delta $length $height tests/teste_"${i}"_"${seed}"

	done
done
fi

#		python synthetic_generator.py 5 5 0 0.1 0.2 3 0 50 100 10 100 100 tests/teste


python common_cluster.py 5 2 0.2 0.4 2 100 500 3 100 100 outfile  # 2.5 dist, cloudssuper4


python common_cluster.py 5 2 0.2 0.4 1 100 500 3 100 100 outfile2
python common_cluster.py 5 2 0.2 0.4 3 100 500 3 100 100 outfile3






























