module eigen90

  use particles

  implicit none

contains  

subroutine eigen(H,EVect)
!========================
! Diagonalisation de matrice symétrique applatie H, de dimension Nvar.
! Ressort les valeurs propres dans H (sur diagonale) et les vecteurs propres dans EVect

  integer :: mv,ind
  integer :: i,j,k,l,m
  integer :: iq,im,il,ij,ia,jq
  integer :: mq,lq,lm,ll,mm
  integer :: ilq,imq,ilr,imr  
  
  real :: anorm,anrmx
  real :: thr
  real :: x,y
  real :: sx,cx,scx

  real, dimension(Nvar*(Nvar+1)/2), intent(INOUT) :: H
  real, dimension(Nvar*Nvar), intent(OUT) :: EVect   

  real(8), parameter :: range=1.d-8

  mv=0
  iq=-Nvar

! On construit une matrice diagonale unitaire

  do j=1,Nvar
    iq=iq+Nvar
    do i=1,Nvar
      ij=iq+i
      EVect(ij)=0.0d0
      if(i==j) EVect(ij)=1.d0
    end do
  end do

  anorm=0.0d0

! On fait la somme des 2 des termes hors diagonale  

  do i=1,Nvar
    do j=i,Nvar
      if(i/=j) then
        ia=i+(j*j-j)/2
        anorm=anorm+H(ia)*H(ia)
      end if
    end do 
  end do
 

  if(anorm>0) then
    anorm=sqrt(2.0d0*anorm)
  else
    go to 165 !la matrice est diagonalisee on va a la fin
  end if 
  
  anrmx=anorm*range/real(Nvar)
  ind=0
  thr=anorm

45 thr=thr/real(Nvar)
50 l=1
55 m=l+1
60 mq=(m*m-m)/2
   lq=(l*l-l)/2
   lm=l+mq
   
   if(abs(H(lm))>=thr) then
     ind=1
   else
     go to 130
   end if

   ll=l+lq
   mm=m+mq
   x=0.5d0*(H(ll)-H(mm))
   y=-H(lm)/sqrt(H(lm)*H(lm)+x*x)

   if(x<0.d0) then
     y=-y
   else
     sx=y/sqrt(2.0d0*(1.0d0+(sqrt(1.0d0-y*y))))
   end if

   cx=sqrt(1.0d0-sx**2)
   scx=sx*cx
   ilq=Nvar*(l-1)
   imq=Nvar*(m-1)

   do i=1,Nvar
     iq=(i*i-i)/2
     if(i/=l) then
       if(i<m) then 
         im=i+mq
       else if(i>m) then
         im=m+iq
       else
         go to 115
       end if

       if(i<l) then
         il=i+lq
       else
         il=l+iq
       end if 

       x=H(il)*cx-H(im)*sx
       H(im)=H(il)*sx+H(im)*cx
       H(il)=x        
     end if

115  if(mv/=1) then
       ilr=ilq+i
       imr=imq+i
       x=EVect(ilr)*cx-EVect(imr)*sx
       EVect(imr)=EVect(ilr)*sx+EVect(imr)*cx
       EVect(ilr)=x
     end if
   end do 
    
   x=2.0d0*H(lm)*scx
   y=H(ll)*cx*cx+H(mm)*sx*sx-x
   x=H(ll)*sx*sx+H(mm)*cx*cx+x
   H(lm)=(H(ll)-H(mm))*scx+H(lm)*(cx*cx-sx*sx)
   H(ll)=y
   H(mm)=x

130 if(m/=Nvar) then
      m=m+1
      go to 60
    else
      if(l/=(Nvar-1)) then
        l=l+1
        go to 55
      else 
        if(ind==1) then
          ind=0
          go to 50
        else 
          if(thr>anrmx) go to 45
        end if
      end if
    end if  

165 iq=-Nvar      

! La matrice est diagonalisee, on reordonne les valeurs propres et les vecteurs propres

    do i=1,Nvar
      iq=iq+Nvar
      ll=i+(i*i-i)/2
      jq=Nvar*(i-2)

      do j=i,Nvar
        jq=jq+Nvar
        mm=j+(j*j-j)/2
        if(H(ll)<H(mm)) then
          x=H(ll)
          H(ll)=H(mm)
          H(mm)=x
          if(mv/=1) then
            do k=1,Nvar
              ilr=iq+k
              imr=jq+k
              x=Evect(ilr)
              Evect(ilr)=Evect(imr)
              Evect(imr)=x
            end do
          end if
        end if
      end do
    end do 

    return

end subroutine eigen
 
end module eigen90
