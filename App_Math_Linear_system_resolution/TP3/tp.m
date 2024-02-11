clear all;
close all;

matrices = ["mat0","mat1","mat2", "mat3", "bcsstk27"];

for nom_matrice = matrices
    
    load(nom_matrice{1})
    fprintf('Analyzing matrix %s...\n', nom_matrice{1});
    
    n = size(A,1);
    figure()
    title(nom_matrice{1});
    % Définir le nom de la fenêtre de figure
    set(gcf, 'Name', nom_matrice{1});
    
    subplot(2, 4, 1);
    spy(A);
    title(sprintf('Original matrix A = %s',nom_matrice{1}));
    
    % Symboic Factorization
    [count, h, parent, post , L] = symbfact(A);
    ALU = L+ L';
    subplot(2, 4, 2)
    spy(ALU);
    title('Factors of A')
    fillin = nnz(ALU) - nnz(A);
    fprintf('Fill-in for A: %d\n', fillin);
    
    % Visualisation du fill-in
    C = spones(A);
    CLU = spones(ALU);
    FILL = CLU - C;
    subplot(2, 4, 3)
    spy(FILL)
    title('Fill on original A')
    
    % Flops during Symbolic Factorization
    flopsSymb = 2*(2*nnz(L)-n);
    fprintf('Flops during Symbolic Factorization for A: %d\n', flopsSymb);
    
    % Cholesky Factorization
    L = chol(A, 'lower');
    
    % Affichage du fill-in suite à la vraie factorisation
    C = spones(triu(A) + L);
    subplot(2, 4, 4)
    spy(C)
    title('L +triu(A)')
    
    b = [1:n]';
    
    % Solution with A
    x1 = A\b;
    
    % Solution with Cholesky Factorization
    x2 = L'\(L\b);
    
    % Flops during Numerical Factorization
    flopsNum = 2*(2*nnz(L)-n);
    fprintf('Flops during Numerical Factorization for A: %d\n', flopsNum);
    
    % Relative Error between the two solutions
    norm(x1-x2)/norm(x1);
    
    % Permutation
    % symamd, symrcm

    P = symamd(A);
    %P= symrcm(A)
    
    % Permute A
    B = A(P, P);
    
    subplot(2, 4, 5);
    spy(B);
    title('Permuted matrix B');
    
    % Symbolic Factorization of B
    [count, h, parent, post, L] = symbfact(B);
    BLU = L + L';
    subplot(2, 4, 6)
    spy(BLU);
    title('Factors of B')
    fillin = nnz(BLU) - nnz(B);
    fprintf('Fill-in for B: %d\n', fillin);
    
    % Visualisation du fill-in
    C = spones(B);
    CLU = spones(BLU);
    FILL = CLU-C;
    subplot(2, 4, 7)
    spy(FILL)
    title('Fill on permuted matrix B')
    
    % Flops during Symbolic Factorization
    flopsSymb = 2*(2*nnz(L)-n);
    fprintf('Flops during Symbolic Factorization for B: %d\n', flopsSymb);
    
    % Cholesky Factorization of B
    L = chol(B,"lower");
    
    % Affichage du fill-in suite à la vraie factorisation
    C = spones(triu(B) + L);
    subplot(2, 4, 8)
    spy(C)
    title('L + triu(B)')
    
    % Solution with permuted B
    x3 = B\b(P);
    x3(P) = x3;
    
    % Solution with Cholesky Factorization of permuted B
    x4 = L'\(L\b(P));
    x4(P) = x4;
    
    % Relative Error between the two solutions
    norm(x4-x3) / norm(x3);
    fprintf('Relative Error between solution of permuted B and original A with cholesky facto: %d\n', norm(x4-x2) / norm(x2))
    fprintf('\n');
    fprintf('\n');
    fprintf('\n');
    fprintf('\n');
    fprintf('\n');
end