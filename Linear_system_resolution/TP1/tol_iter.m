close all;
clear all;

% Matrices à résoudre
matrices = {'mat1', 'pde225_5e-1', 'hydcar20'};

% Tolérances à tester
tolerances = logspace(-3, -14, 20);

for nom_matrice = matrices
    load(nom_matrice{1})
    n = size(A,1);
    fprintf('dimension de A : %4d \n' , n);

    b = [1:n]';

    x0 = zeros(n, 1);

    itermax = 2*n;
    
    %iterations en fonction des tolérances
    list_iterfom=[];
    list_itergmres = [];
    figure()
    for i = 1:length(tolerances)
        tolr = tolerances(i);
        % FOM
        [x, flag, relres, iter_fom, resvec] = krylov(A, b, x0, tolr, itermax, 0);
        list_iterfom(i) = iter_fom;
    
        % GMRES
        [x, flag, relres, iter_gmres, resvec] = krylov(A, b, x0, tolr, itermax, 1);
        list_itergmres(i) = iter_gmres;
            
    end
    loglog(tolerances,list_iterfom, 'o');
    hold on
    loglog(tolerances, list_itergmres, 'x');
    xlabel('tolerances');
    ylabel('iterations');
    title(sprintf('Nb itérations en fonction de la tolérance - Matrice : %s', nom_matrice{1}));
    legend('FOM', 'GMRES');
    grid on;
end