
function [x, flag, relres, iter, resvec] = krylov(A, b, x0, tol, maxit, type)
% Résolution de Ax = b par une méthode de Krylov

% x      : solution
% flag   : convergence (0 = convergence, 1 = pas de convergence en maxit)
% relres : résidu relatif (backward error normwise)
% iter   : nombre d'itérations
% resvec : vecteur contenant les iter normes du résidu


% A     :matrice du système
% b     : second membre
% x0    : solution initiale
% tol   : seuil de convergence (pour l'erreur inverse)
% maxit : nombre d'itérations maximum
% type : méthode de Krylov
%        type == 0  FOM
%        type == 1  GMRES

n = size(A, 2);
r0 = b - A*x0;
beta = norm(r0);
normb = norm(b);
% résidu relatif backward erreur normwise
relres = beta / normb;
% matlab va agrandir de lui même le vecteur resvec et les matrices V et H
resvec(1) = beta;
resvec_estime(1) = beta;
V(:,1) = r0 / beta;
j = 1;
x = x0;

while (j<maxit) && (relres>tol) % critère d'arrêt
    
    w = A*V(:,j);
    
    % orthogonalisation (Modified Gram-Schmidt)
    for i = 1:j 
        H(i,j) = V(:,i)'*w;
        w = w - H(i,j)*V(:,i);
    end
    % calcul de H(j+1, j) et normalisation de V(:, j+1)
    H(j+1,j) = norm(w);
    V(:,j+1) = w/H(j+1,j) ;
    % suivant la méthode
    if(type == 0)
        % FOM
        % résolution du système linéaire H.y = beta.e1
        % construction de beta.e1 (taille j)
        e1 = zeros(j,1) ;
        e1(1) = 1 ;
        beta_e1 = beta*e1;
        % résolution de H.y = beta.e1 avec '\'
        y = H(1:j,1:j)\beta_e1 ;

        %calcul du résidu estimé pour l'algo FOM
        ej = zeros(j,1);
        ej(j) = 1;
        %resvec_estime(j+1) = H(j+1,j)*abs(ej'*y);
    else
        % GMRES
        % résolution du problème aux moindres carrés argmin ||beta.e1 - H_barre.y||
        % construction de beta.e1 (taille j+1)
        e1 = zeros(j+1,1) ;
        e1(1) = 1 ;
        beta_e1 = beta*e1;
        % résolution de argmin ||beta.e1 - H_barre.y|| avec '\'
        y = H(1:j+1,:)\beta_e1 ;

        %calcul du résidu estimé pour l'algo GMRES
        [Q,R]= qr(H) ;
        g_barre = Q'*beta_e1;
        %y = R(1:j, 1:j)\g_barre(1:j);
        %resvec_estime(j+1) = abs(g_barre(j+1));
        
        
    end
    
    % calcul de l'itérée courant x 
    x = x0 + V(:,1:j)*y ;

    % calcul du résidu et rangement dans resvec
    resvec(j+1) = norm(A*x-b) ;
    
    %résidu estimé
    %resvec(j+1) = resvec_estime(j+1);
    
    % calcul du résidu relatif (backward error) relres
    relres = resvec(j+1)/normb;
    j= j+1;
    
end

% le nombre d'itération est j - 1 (imcrément de j en fin de boucle)
iter = j-1;

% positionnement du flac suivant comment on est sortie de la boucle
if(relres > tol)
    flag = 1;
else
    flag = 0;
end
