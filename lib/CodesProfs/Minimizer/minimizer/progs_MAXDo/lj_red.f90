module lj_red

  use particles
  use compute_distance
  use run_parameter
  
  implicit none

  contains
 
subroutine force_LJ
!==================
 
  integer :: i,j
  integer :: parti,partj
  integer :: proti,protj

  real(8) ::  xi,yi,zi,xj,yj,zj
  real(8) ::  dx,dy,dz,r_2

  character*1 chaini
  character*1 chainj

  fx_lj(:)=0.0d0; fy_lj(:)=0.0d0; fz_lj(:)=0.0d0 

   do parti=1,N_particle-1
    
    xi=molecule(parti)%x
    yi=molecule(parti)%y
    zi=molecule(parti)%z

    chaini=residue(parti)%chain
    proti=residue(parti)%prot

    do partj=parti+1,N_particle

      xj=molecule(partj)%x
      yj=molecule(partj)%y
      zj=molecule(partj)%z

      chainj=residue(partj)%chain
      protj=residue(partj)%prot

      if(proti/=protj) then
 
        call distance(xi,yi,zi,xj,yj,zj,dx,dy,dz,r_2)

        fx_lj(parti)=fx_lj(parti)+force_x_red_lj(dx,dy,dz,r_2,parti,partj)
        fy_lj(parti)=fy_lj(parti)+force_y_red_lj(dx,dy,dz,r_2,parti,partj)
        fz_lj(parti)=fz_lj(parti)+force_z_red_lj(dx,dy,dz,r_2,parti,partj)
         
        fx_lj(partj)=fx_lj(partj)-force_x_red_lj(dx,dy,dz,r_2,parti,partj)
        fy_lj(partj)=fy_lj(partj)-force_y_red_lj(dx,dy,dz,r_2,parti,partj)
        fz_lj(partj)=fz_lj(partj)-force_z_red_lj(dx,dy,dz,r_2,parti,partj)

      end if          
    end do
  end do

  return

end subroutine force_LJ

subroutine LJpot(Elj)
!====================

  real(8), intent(OUT) :: Elj

  real(8) ::  energy
  real(8) ::  xi,yi,zi
  real(8) ::  xj,yj,zj
  real(8) ::  dx,dy,dz
  real(8) ::  Ai,Aj
  real(8) ::  Bij, Cij
  real(8) ::  ri,rj
  real(8) ::  r_2
  real(8) ::  temp_factor
  
  integer :: i,j,proti,protj 

  character*1 chaini
  character*1 chainj

  temp_factor=temp_pot*0.596

  Elj=0.d0
  energy=0.d0

  do i=1,N_particle-1

    ri=molecule(i)%radius
    Ai=molecule(i)%energy

    xi=molecule(i)%x
    yi=molecule(i)%y
    zi=molecule(i)%z

    chaini=residue(i)%chain
    proti=residue(i)%prot 
 
    do j=i+1,N_particle

      rj=molecule(j)%radius
      Aj=molecule(j)%energy

      xj=molecule(j)%x
      yj=molecule(j)%y
      zj=molecule(j)%z

      chainj=residue(j)%chain
      protj=residue(j)%prot 

      if(proti/=protj) then
!      if(chaini/=chainj) then

        call distance(xi,yi,zi,xj,yj,zj,dx,dy,dz,r_2)
 
        if(r_2<=sigmacut**2) then
         
          Bij=Ai*Aj*((ri+rj)**8)
          Cij=Ai*Aj*((ri+rj)**6)

          energy=Bij/(r_2**4)-Cij/(r_2**3)           
          Elj=Elj+energy
        end if    
      end if
    end do
  end do

  Elj=temp_factor*Elj*lambda

  return

end subroutine LJpot

real(8) function force_x_red_lj(dx,dy,dz,r_2,i,j)
!=============================================

  integer, intent(IN) :: i,j
  real(8), intent(IN) :: dx,dy,dz,r_2

  real(8) ::  Aij, Rij, Bij, Cij
  real(8) ::  r_ij

  Aij=molecule(i)%energy*molecule(j)%energy
  Rij=molecule(i)%radius+molecule(j)%radius
  Bij=Aij*(Rij**8)
  Cij=Aij*(Rij**6)

  force_x_red_lj=lambda*(8.0*Bij/r_2**4-6.0*Cij/r_2**3)*dx/r_2

  return  

end function force_x_red_lj

real(8) function force_y_red_lj(dx,dy,dz,r_2,i,j)
!=============================================

  integer, intent(IN) :: i,j
  real(8), intent(IN) :: dx,dy,dz,r_2

  real(8) ::  Aij, Rij, Bij, Cij
  real(8) ::  r_ij

  Aij=molecule(i)%energy*molecule(j)%energy
  Rij=molecule(i)%radius+molecule(j)%radius
  Bij=Aij*(Rij**8)
  Cij=Aij*(Rij**6)

  force_y_red_lj=lambda*(8.0*Bij/r_2**4-6.0*Cij/r_2**3)*dy/r_2

  return  

end function force_y_red_lj

real(8) function force_z_red_lj(dx,dy,dz,r_2,i,j)
!=============================================

  integer, intent(IN) :: i,j
  real(8), intent(IN) :: dx,dy,dz,r_2

  real(8) ::  Aij, Rij, Bij, Cij
  real(8) ::  r_ij

  Aij=molecule(i)%energy*molecule(j)%energy
  Rij=molecule(i)%radius+molecule(j)%radius
  Bij=Aij*(Rij**8)
  Cij=Aij*(Rij**6)

  force_z_red_lj=lambda*(8.0*Bij/r_2**4-6.0*Cij/r_2**3)*dz/r_2

  return  

end function force_z_red_lj


end module lj_red
