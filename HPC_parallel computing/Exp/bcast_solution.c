  // char *bcast_implementation_name:   the bcast implementation name (argument #1)
  // int chunk_size:                    the chunk size (optional argument #2)
  // int NUM_BYTES:                     the number of bytes to broadcast
  // char *buffer:                      the buffer to broadcast

  // Process rank 0 should be the source of the broadcast

  // Default Broadcast
  if(strcmp(bcast_implementation_name, "default_bcast") == 0) {

    MPI_Bcast(buffer, NUM_BYTES, MPI_BYTE, 0, MPI_COMM_WORLD);

  }

  // Naive Broadcast
  if(strcmp(bcast_implementation_name, "naive_bcast") == 0) {

    if (rank == 0) {
        // Send the buffer to all other processes
        for (int dest = 1; dest < num_procs; dest++) {
            MPI_Ssend(buffer, NUM_BYTES, MPI_BYTE, dest, 0, MPI_COMM_WORLD);
        }
    } else {
        // Receive the buffer from the root process
        MPI_Recv(buffer, NUM_BYTES, MPI_BYTE, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    
    }
  }
  
  // Ring Broadcast
  if(strcmp(bcast_implementation_name, "ring_bcast") == 0) {

    if (rank == 0) {
        // Send the buffer to the next process in the ring
        MPI_Ssend(buffer, NUM_BYTES, MPI_BYTE, (rank + 1) % num_procs, 0, MPI_COMM_WORLD);
    } else {
        // Receive the buffer from the previous process in the ring
        MPI_Recv(buffer, NUM_BYTES, MPI_BYTE, (rank - 1 + num_procs) % num_procs, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        // Send the buffer to the next process in the ring (except for the last process)
        if (rank != num_procs - 1) {
            MPI_Ssend(buffer, NUM_BYTES, MPI_BYTE, (rank + 1) % num_procs, 0, MPI_COMM_WORLD);
        }
    }
    
  }

  // Bintree Broadcast
  if (strcmp(bcast_implementation_name, "bintree_bcast") == 0) {
     int root = (rank-1)/2;
     int left = 2 * rank + 1;
     int right = 2 * rank + 2;
     
    if (rank==0) {
        if (left < num_procs){
            //left child exists
            //send buffer
           MPI_Ssend(buffer, NUM_BYTES, MPI_BYTE, left, 0, MPI_COMM_WORLD);
        }
        if (right < num_procs){
            //right child exists
            //send buffer
           MPI_Ssend(buffer, NUM_BYTES, MPI_BYTE, right, 0, MPI_COMM_WORLD);
        }
    }
    else {
        MPI_Recv(buffer, NUM_BYTES, MPI_BYTE, root, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        if (left < num_procs){
            //left child exists
            //send buffer
           MPI_Ssend(buffer, NUM_BYTES, MPI_BYTE, left, 0, MPI_COMM_WORLD);
        }
        if (right < num_procs){
            //right child exists
            //send buffer
           MPI_Ssend(buffer, NUM_BYTES, MPI_BYTE, right, 0, MPI_COMM_WORLD);
        }
    }

  }
  
  // Pipelined Ring Broadcast
  if(strcmp(bcast_implementation_name, "pipelined_ring_bcast") == 0) {
     if (NUM_BYTES % chunk_size != 0){
      printf("error : %d doesn't divide %d\n", chunk_size, NUM_BYTES);
      MPI_Finalize();
    }

    int nb_packages = NUM_BYTES/chunk_size;
    int stride;
    if (rank == 0){
      printf("nombre de paquets %d\n", nb_packages);
      stride = 0;
      for (int i = 0; i < nb_packages; i++){
        MPI_Ssend(buffer + stride, chunk_size, MPI_BYTE, rank+1, 0, MPI_COMM_WORLD);
        stride += chunk_size;
      }
    } else if(rank == num_procs - 1){
      stride = 0;
      for (int i = 0; i < nb_packages; i++){
        MPI_Recv(buffer+stride, chunk_size, MPI_BYTE, rank-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        stride += chunk_size;
      }
    } else{
      stride = 0;
      for (int i = 0; i < nb_packages; i++){
        MPI_Recv(buffer+stride, chunk_size, MPI_BYTE, rank-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Ssend(buffer + stride, chunk_size, MPI_BYTE, rank+1, 0, MPI_COMM_WORLD);
        stride += chunk_size;
      }
    }
    
  }
  
  // Non-Blocking Pipelined Ring Broadcast
   if(strcmp(bcast_implementation_name, "non_blocking_pipelined_ring_bcast") == 0) {


      if (NUM_BYTES%chunk_size != 0) {
        printf("NUM_BYTES must be divisible by chunk_size\n");
        MPI_Finalize();
      }
      int num_chunks = NUM_BYTES/chunk_size;
      int i;
      MPI_Request requests[num_chunks];
    
      if (rank == 0){
        for (i = 0; i < num_chunks; i++) {
          MPI_Isend(buffer+i*chunk_size, chunk_size, MPI_BYTE, 1, 0, MPI_COMM_WORLD, &requests[i]);
        }for (i = 0; i < num_chunks; i++) {
          MPI_Wait(&requests[i], MPI_STATUS_IGNORE);
        }
      } else if (rank == num_procs-1) {
        for (i = 0; i < num_chunks; i++) {
          MPI_Recv(buffer+i*chunk_size, chunk_size, MPI_BYTE, rank-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
      } else {
        for (i = 0; i < num_chunks; i++) {
          MPI_Recv(buffer+i*chunk_size, chunk_size, MPI_BYTE, rank-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
          MPI_Isend(buffer+i*chunk_size, chunk_size, MPI_BYTE, rank+1, 0, MPI_COMM_WORLD, &requests[i]);
        }
        MPI_Waitall(num_chunks, requests, MPI_STATUSES_IGNORE);
      }
    }
  // Non-Blocking Pipelined Bintree Broadcast
  if(strcmp(bcast_implementation_name, "non_blocking_pipelined_bintree_bcast") == 0) {
    
    int root = (rank-1)/2;
    int left = 2 * rank + 1;
    int right = 2 * rank + 2;
    
    if (NUM_BYTES % chunk_size != 0){
      printf("Warning: %d doesn't divide %d\n", chunk_size, NUM_BYTES);
      MPI_Finalize();

    } 
    
    MPI_Request request[NUM_BYTES/chunk_size];
     
    if (rank==0) {
        if (left < num_procs){
            //left child exists
            for (i = 0; i < (NUM_BYTES/chunk_size); i++){
              MPI_Isend(buffer + i*chunk_size, chunk_size, MPI_BYTE, left, 0, MPI_COMM_WORLD, &request[i]); 
            }
            
            for (i = 0; i < (NUM_BYTES/chunk_size); i++){
              MPI_Wait(request, MPI_STATUS_IGNORE);
            }   
        }
        if (right < num_procs){
            //right child exists
           for (i = 0; i < (NUM_BYTES/chunk_size); i++){
              MPI_Isend(buffer + i*chunk_size, chunk_size, MPI_BYTE, right, 0, MPI_COMM_WORLD, &request[i]); 
            }
            
            for (i = 0; i < (NUM_BYTES/chunk_size); i++){
              MPI_Wait(request, MPI_STATUS_IGNORE);
            }   
        }
    }
    else {

        for (i = 0; i < (NUM_BYTES/chunk_size); i++){
          MPI_Recv(buffer+i*chunk_size, chunk_size, MPI_BYTE, root, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }   
        if (left < num_procs){
            //left child exists
           for (i = 0; i < (NUM_BYTES/chunk_size); i++){
              MPI_Isend(buffer + i*chunk_size, chunk_size, MPI_BYTE, left, 0, MPI_COMM_WORLD, &request[i]);
           }
           for (i = 0; i < (NUM_BYTES/chunk_size); i++){
              MPI_Wait(&request[i], MPI_STATUS_IGNORE);
           }
        }
        if (right < num_procs){
            //right child exists
           for (i = 0; i < (NUM_BYTES/chunk_size); i++){
              MPI_Isend(buffer + i*chunk_size, chunk_size, MPI_BYTE, right, 0, MPI_COMM_WORLD, &request[i]);
           }
           for (i = 0; i < (NUM_BYTES/chunk_size); i++){
              MPI_Wait(&request[i], MPI_STATUS_IGNORE);
           }
       }
   }

  }
