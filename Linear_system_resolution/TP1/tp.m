close all;
clear all;

% Matrices à résoudre
matrices = {'mat1', 'pde225_5e-1', 'hydcar20'};
% Tolérance
tol = 1e-6 ;
% Ensemble de tolérances à tester
tolerances = logspace(-3, -14, 20);


for nom_matrice = matrices
    load(nom_matrice{1})
    n = size(A,1);
    fprintf('dimension de A : %4d \n' , n);

    b = [1:n]';

    x0 = zeros(n, 1);

    kmax = 2*n;
    
    figure()
    
    fprintf('Tolérance : %g \n', tol);
    
    % FOM
    [x, flag, relres, iter, resvec] = krylov(A, b, x0, tol, kmax, 0);
    fprintf('FOM - Nb iterations : %4d \n' , iter);
    semilogy(resvec, 'c');
    hold on
    if(flag == 1)
      fprintf('pas de convergence\n');
    end

    % GMRES
    [x, flag, relres, iter, resvec] = krylov(A, b, x0, tol, kmax, 1);
    fprintf('GMRES - Nb iterations : %4d \n' , iter);
    semilogy(resvec, 'r');
    hold on
    if(flag == 1)
      fprintf('pas de convergence\n');
    end

    % GMRES Matlab
    [x, flag, relres, iter, resvec] = gmres(A, b, [], tol, kmax, [], [], x0);
    fprintf('GMRES Matlab - Nb iterations : %4d \n' , iter);
    semilogy(resvec, '.y');
    hold on
    if(flag == 1)
      fprintf('pas de convergence\n');
    end

    xlabel('iterations');
    ylabel('norme résidu estimée');
    title(sprintf('Tolérance : %g - Matrice : %s', tol, nom_matrice{1}));
    legend('FOM', 'GMRES', 'GMRES Matlab');
    drawnow;
    
end
