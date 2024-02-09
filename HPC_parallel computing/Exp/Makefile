SMPICC=smpicc
SMPIRUN=smpirun
PWD=$(shell pwd)
#SMPICC = docker run --rm -it --mount type=bind,source=$(PWD),target=/home/smpi henricasanova/ics632_smpi smpicc
#SMPIRUN = docker run --rm -it --mount type=bind,source=$(PWD),target=/home/smpi henricasanova/ics632_smpi smpirun



default: 
	@echo "make activity1 (naive, ring, default)" 
	@echo "make activity2 (pipelined ring)"
	@echo "make activity3 (non blocking pipelined ring)"
	@echo "make activity4 (non blocking pipelined bintree)"
	@echo "make activity5 (cluster)"
	

SMPI_FLAGS=--cfg=smpi/bcast:mpich

bcast_skeleton: bcast_skeleton.c bcast_solution.c
	$(SMPICC) bcast_skeleton.c -o bcast_skeleton

STDERR = 2> /dev/null
#STDERR = 


CHUNKSIZES= 100000 500000 1000000 5000000 10000000 50000000 100000000

SHUFFLE=no

activity1: bcast_skeleton
	@echo "**** ACTIVITY #1 ****"
	@$(eval NP=50)
	./generate_xml_ring_and_hostfile.py $(NP) $(STDERR)
	@$(eval PLATFORM_FLAGS=-np $(NP) -hostfile hostfile_$(NP).txt -platform ./ring_$(NP).xml)
	@echo "Executions with $(NP) processes:"
	@$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton naive_bcast $(STDERR) 
	@$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton ring_bcast $(STDERR)
	@$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton default_bcast  $(STDERR)
	@echo "--"

activity2: bcast_skeleton
	@echo "**** ACTIVITY #2 ****"
	@$(eval NP=20)
	@./generate_xml_ring_and_hostfile.py $(NP) 
	@echo "Executions with $(NP) processes:"
	@$(eval PLATFORM_FLAGS=-np $(NP) -hostfile hostfile_$(NP).txt -platform ./ring_$(NP).xml)
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton pipelined_ring_bcast -c $$chunksize $(STDERR) ; \
	done
	@$(eval NP=35)
	@./generate_xml_ring_and_hostfile.py $(NP) $(STDERR)
	@echo "Executions with $(NP) processes:"
	@$(eval PLATFORM_FLAGS=-np $(NP) -hostfile hostfile_$(NP).txt -platform ./ring_$(NP).xml)
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton pipelined_ring_bcast -c $$chunksize $(STDERR) ; \
	done
	@$(eval NP=50)
	@./generate_xml_ring_and_hostfile.py $(NP) $(STDERR)
	@echo "Executions with $(NP) processes:"
	@$(eval PLATFORM_FLAGS=-np $(NP) -hostfile hostfile_$(NP).txt -platform ./ring_$(NP).xml)
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton pipelined_ring_bcast -c $$chunksize $(STDERR) ; \
	done
	@echo "--"

activity3: bcast_skeleton
	@echo "**** ACTIVITY #3 ****"
	@$(eval NP=50)
	@./generate_xml_ring_and_hostfile.py $(NP) $(STDERR)
	@echo "Executions with $(NP) processes:"
	@$(eval PLATFORM_FLAGS=-np $(NP) -hostfile hostfile_$(NP).txt -platform ./ring_$(NP).xml)
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton non_blocking_pipelined_ring_bcast -c $$chunksize $(STDERR) ; \
	done
	@echo "--"

activity4: bcast_skeleton
	@echo "**** ACTIVITY #4 ****"
	@$(eval NP=50)
	@./generate_xml_ring_and_hostfile.py $(NP) $(STDERR)
	@./generate_xml_bintree_and_hostfile.py $(NP) $(STDERR)
	@echo "Executions with $(NP) processes on a ring platform:"
	@$(eval PLATFORM_FLAGS=-np $(NP) -hostfile hostfile_$(NP).txt -platform ./ring_$(NP).xml)
	@$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton default_bcast $(STDERR)
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton non_blocking_pipelined_ring_bcast -c $$chunksize $(STDERR) ; \
	done
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton non_blocking_pipelined_bintree_bcast -c $$chunksize $(STDERR) ; \
	done
	@echo "--"
	@echo "Executions with $(NP) processes on a bintree platform:"
	@$(eval PLATFORM_FLAGS=-np $(NP) -hostfile hostfile_$(NP).txt -platform ./bintree_$(NP).xml)
	@$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton default_bcast $(STDERR)
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton non_blocking_pipelined_ring_bcast -c $$chunksize $(STDERR) ; \
	done
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton non_blocking_pipelined_bintree_bcast -c $$chunksize $(STDERR) ; \
	done
	@echo "--"


activity5: bcast_skeleton
	echo "**** ACTIVITY #5 ****"
	cp ../cluster*.xml .
	cp ../hostfile_64.txt .
	@$(eval NP=64)
	@$(eval PLATFORM_FLAGS=-np $(NP) -hostfile hostfile_$(NP).txt -platform ./cluster_crossbar_$(NP).xml)
	@echo "Executions with $(NP) processes on a cluster crossbar platform:"
	@$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton default_bcast $(STDERR)
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton non_blocking_pipelined_ring_bcast -c $$chunksize $(STDERR) ; \
	done
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton non_blocking_pipelined_bintree_bcast -c $$chunksize $(STDERR) ; \
	done
	@$(eval PLATFORM_FLAGS=-np $(NP) -hostfile hostfile_$(NP).txt -platform ./cluster_backbone_$(NP).xml)
	@echo "Executions with $(NP) processes on a cluster backbone platform:"
	@$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton default_bcast $(STDERR)
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton non_blocking_pipelined_ring_bcast -c $$chunksize $(STDERR) ; \
	done
	@for chunksize in $(CHUNKSIZES) ; do \
		$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_skeleton non_blocking_pipelined_bintree_bcast -c $$chunksize $(STDERR) ; \
	done
	@echo "--"

		
SAVE:
	@echo "--- RANDOMIZED HOSTFILE ---"
	@cat hostfile_$(NP).txt | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' > tmp; mv tmp host_file$(NP)
	@$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_default -s "bcast_default|ring_$(NP)|" $(STDERR)
	@$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_naive -s "bcast_naive|ring_$(NP)|" $(STDERR)
	@$(SMPIRUN) $(SMPI_FLAGS) $(PLATFORM_FLAGS) ./bcast_ring -s "bcast_ring|ring_$(NP)|" $(STDERR)


clean:
	/bin/rm -f ./bcast_skeleton *_*.xml hostfile_* tmp* README.aux README.log  README.pdf

