#!/bin/bash

pdnndir=/home/lukasschmit/pdnn
device=gpu0

export PYTHONPATH=$PYTHONPATH:$pdnndir
export THEANO_FLAGS=mode=FAST_RUN,device=$device,floatX=float32,fastmath=True

# model counter
i=0

for a in "1x350x4:12,16x4,p2x1:6,6x1,p2x1,f" "1x350x4:16,16x4,p2x1:6,6x1,p2x1,f" "1x350x4:24,16x4,p2x1:6,6x1,p2x1,f" "1x350x4:12,16x4,p2x1:12,12x1,p2x1,f" "1x350x4:16,16x4,p2x1:12,12x1,p2x1,f" "1x350x4:24,16x4,p2x1:12,12x1,p2x1,f"
do
	for b in 64 1
	do
		for l in "MD:0.5:0.5:0.01,0.0001:30" "MD:0.1:0.5:0.01,0.0001:30" "MD:0.01:0.5:0.01,0.0001:30"
		do
			for r in 0.0 0.001
			do
				for m in 0.0 0.5
				do
					printf "Model #%i:\n" $i
					printf "Training model...\n"

					# train model
					python $pdnndir/cmds/run_CNN.py \
					            --train-data "./BinaryData/training.pkl.gz,random=True" \
                                --valid-data "./BinaryData/validation.pkl.gz,random=True" \
                                --conv-nnet-spec $a \
                                --nnet-spec "1:2" \
                                --wdir ./logs/ \
                                --l2-reg $r \
                                --lrate $l \
                                --model-save-step 1 \
                                --param-output-file "./logs/cnn$i.param" \
                                --cfg-output-file "./logs/cnn$i.cfg" \
                                --batch-size $b \
                                --momentum $m >& "./logs/train_log$i.txt"

                    printf "Testing model...\n"
                    pwd

                    # run test set
					python $pdnndir/cmds/run_Extract_Feats.py \
					            --data "./BinaryData/test.pkl.gz" \
                                --nnet-param "./logs/cnn$i.param" \
                                --nnet-cfg "./logs/cnn$i.cfg" \
                                --output-file "./logs/cnn$i.classify.pkl.gz" \
                                --layer-index -1 \
                                --batch-size 100 >& "./logs/test_log$i.txt"
 
                    cd ./logs

                    # print model info
                    python ../print_error.py "cnn$i.classify.pkl.gz"
                    printf "Archtecture: %s\n" $a
                    printf "Batch: %i\n" $b 
                    printf "LearningRate: %s\n" $l
                    printf "Regularization: %f\n\n" $r

                    # move back to training directory
                    cd ../

                    ((i++))
				done
			done
		done
	done
done

printf "Finished training %i models." $i
