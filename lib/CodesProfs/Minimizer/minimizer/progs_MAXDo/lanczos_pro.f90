module lanczos_pro

  use run_parameter
  use particles
  use random
  use energa
 
  implicit none
  
  contains
  
subroutine lanczos(maxvec,new_projection,projection)
!===================================================

  integer, intent(IN) :: maxvec, new_projection
  real(8), dimension(Nvar), intent(INOUT) :: projection

  integer, dimension(maxvec) :: iscratch
  real(8), dimension( 2 * maxvec -1 ) :: scratcha
  real(8), dimension(maxvec) :: diag
  real(8), dimension(maxvec) :: eigenvals 
  real(8), dimension(maxvec-1) :: offdiag
  real(8), dimension(Nvar) ::old_projection 
  real(8), dimension(maxvec, maxvec) :: vector
  real(8), dimension(Nvar,maxvec), target :: lanc, proj

! Vectors used to build the matrix for Lanzcos algorithm 
  real(8), dimension(:), pointer :: z0, z1, z2
 
  integer :: i,j,k, i_err, scratcha_size,ivec,size
!ifdef IBM
  integer :: nscratch,length_upper,choice, index
  real(8), dimension(2*maxvec) :: scratch
  real(8), dimension(maxvec*(maxvec+1)/2) :: upper
!endif
  real(8) :: Elj, Eelec
  real(8) :: a1,a0,b2,b1,increment
  real(8) :: excited_energy
  real(8) :: xsum, ysum, zsum, sum2, invsum
  real(8), dimension(Nvar) :: newpos,newforce,ref_force,grad
  real(8) :: ran3, c1, norm

  increment = 0.001  ! Increment

  ! We now take the current position as the reference point and will make 
  ! a displacement in a random direction or using the previous direction as
  ! the starting point.

!  call calcforce(pos,ref_force,total_energy,ener,fohig)
  call energy(Lig_position,total_energy,Elj,Eelec,grad)
  ref_force(:)=-grad(:)  
!   call calcforce(pos,ref_force,total_energy,autres_en,fohig,folow,ehigh)
!  call calcforce(NATOMS,type,pos,boxl,ref_force,total_energy)
  evalf_number = evalf_number + 1
  z0 => lanc(:,1)

   !write(*,201) projection
   !201 format(1x, 3f12.6)

  if(new_projection > 0 ) then
    z0 = projection             ! Vectorial operation
    old_projection = projection ! Vectorial operation
  else
    do i=1,Nvar
      z0(i) = 0.5d0 - ranval()
    end do

    z1 => lanc(1,:)

    if(first_time) then
      old_projection = z0   ! Vectorial operation
      first_time = .false.
    else
      old_projection = projection
    endif 
  endif

  ! We normalize the displacement to 1 total
  sum2=0.d0
  sum2=dot_product(z0,z0)

  invsum = 1.0/sqrt(sum2)
  z0 = z0 * invsum

  newpos = Lig_position + z0 * increment   ! Vectorial operation
!  call calcforce(newpos,newforce,excited_energy,ener,fohig)
  call energy(newpos,excited_energy,Elj,Eelec,grad)
  newforce(:)=-grad(:)
! call calcforce(newpos,newforce,excited_energy,autres_en,fohig,folow,ehigh)
  evalf_number = evalf_number + 1
  
  ! We extract lanczos(1)
  newforce = newforce - ref_force  

  ! We get a0
  a0=0.d0
  a0=dot_product(z0,newforce)
  diag(1)=a0

  z1 => lanc(:,2)
  z1 = newforce - a0 * z0    ! Vectorial operation

  b1=0.d0
  b1=dot_product(z1,z1)
  offdiag(1) = sqrt(b1)

  invsum = 1.0d0 / sqrt ( b1 )
  z1 = z1 * invsum           ! Vectorial operation
  
  ! We can now repeat this game for the next vectors
  do ivec = 2, maxvec-1
    z1 => lanc(:,ivec)
    newpos = Lig_position + z1 * increment
!    call calcforce(newpos,newforce,excited_energy,ener,fohig) 
    call energy(newpos,excited_energy,Elj,Eelec,grad)
    newforce=-grad  
   !call calcforce(newpos,newforce,excited_energy,autres_en,fohig,folow,ehigh)
    evalf_number = evalf_number + 1
    newforce = newforce - ref_force  

    a1 = 0.d0
    a1=dot_product(z1,newforce)
    diag(ivec) = a1

    b1 = offdiag(ivec-1)
    z0 => lanc(:,ivec-1)
    z2 => lanc(:,ivec+1)
    z2 = newforce - a1*z1 -b1*z0

    b2=0.0d0
    b2=dot_product(z2,z2)
    offdiag(ivec) = sqrt(b2)
    
    invsum = 1.0/sqrt(b2)
    z2 = z2 * invsum
  end do

  ! We now consider the last line of our matrix
  ivec = maxvec
  z1 => lanc(:,maxvec)
  newpos = Lig_position + z1 * increment    ! Vectorial operation
!  call calcforce(newpos,newforce,excited_energy,ener,fohig)
  call energy(newpos,excited_energy,Elj,Eelec,grad)
  newforce=-grad 
!  call calcforce(newpos,newforce,excited_energy,autres_en,fohig,folow,ehigh)
  evalf_number = evalf_number + 1
  newforce = newforce - ref_force

  a1 = 0.0d0
  a1=dot_product(z1,newforce)
  diag(maxvec) = a1

  ! We now have everything we need in order to diagonalise and find the
  ! eigenvectors.

  diag = -1.0d0 * diag
  offdiag = -1.0d0 * offdiag

  ! We now need the routines from Lapack. We define a few values
  i_err = 0

  ! We call the routine for diagonalizing a tridiagonal  matrix

!#ifdef IBM
!!!  CHANGE FOR IA32 PC
  ! If run on an IBM, must use a different lapack routine. 
  ! Since we have a tridiagonal matrix, all elements but a few are zero 
  length_upper = maxvec * (maxvec+1) / 2
!  nscratch = 2 * maxvec;
!  upper = 0.0   ! Vectorial operation

  
  ! And we add the diagonal and off-diagonal elements 
!  index = 1
!  do i=1, maxvec
!    upper(index) = diag(i)
!    index = index  + (maxvec-i+1)
!  end do

!  index = 1
!  do i=1, (maxvec-1)
!    upper(index+1) = offdiag(i)
!    index = index + (maxvec-i + 1)
!  end do

!   choice = 1;
!  call dspev(choice,upper,diag,vector,maxvec,maxvec,scratch,nscratch)
!#else
  call dstev('V',maxvec,diag,offdiag,vector,maxvec,scratcha,i_err)
!#endif
  ! We now reconstruct the eigenvectors in the real space
  ! Of course, we need only the first maxvec elements of vec

  projection = 0.0d0    ! Vectorial operation
  do k=1, maxvec
    z1 => lanc(:,k)
    a1 = vector(k,1)
    projection = projection + a1 * z1   ! Vectorial operation
  end do 
  
!  c1=0.0d0
!  do i=1, VECSIZE
!    c1 = c1 + projection(i) * projection(i)
!  end do
!  c1 = sqrt(c1)
!  write(*,*)' norm of projection', c1 

!  norm = 1.0d0 / sqrt ( c1 )
!  projection = projection * norm           ! Vectorial operation

  ! The following lines are probably not needed.
  newpos = Lig_position + projection * increment   ! Vectorial operation
!  call calcforce(newpos,newforce,excited_energy,ener,fohig)
  call energy(newpos,excited_energy,Elj,Eelec,grad)
  newforce=-grad
!  call calcforce(newpos,newforce,excited_energy,autres_en,fohig,folow,ehigh) 
  evalf_number = evalf_number + 1
  newforce = newforce - ref_force

  eigenvalue=diag(1)/increment
  do i=1, 4
    eigenvals(i) = diag(i) / increment
  end do

  a1=0.0d0
  a1=dot_product(old_projection,projection)
  
  if(a1<0.0d0) projection = -1.0d0 * projection 
  
!  size = VECSIZE 
!  call center(projection, size)

  return 
 
end subroutine lanczos

end module lanczos_pro
