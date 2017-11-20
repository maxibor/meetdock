module born

  use particles
  use compute_distance
  use run_parameter

  implicit none

  contains

subroutine SPLelec(Ecoul)
!========================

  real(8), intent(OUT) :: Ecoul

  real(8) ::  coul
  real(8) ::  qi,qj
  real(8) ::  ri,rj,r_2
  real(8) ::  xi,yi,zi
  real(8) ::  xj,yj,zj
  real(8) ::  dx,dy,dz

  integer :: i,j
  integer :: proti,protj

  character*1 :: chi,chj
  
  Ecoul=0.d0

  do i=1,N_particle-1
    
    xi=molecule(i)%x
    yi=molecule(i)%y
    zi=molecule(i)%z

    chi=residue(i)%chain
    proti=residue(i)%prot
    qi=molecule(i)%charge

    if(qi/=0.0) then

      do j=i+1,N_particle
 
        chj=residue(j)%chain
        protj=residue(j)%prot
        qj=molecule(j)%charge

        if(qj/=0.0.and.proti/=protj) then
!        if(qj/=0.0.and.chi/=chj) then
 
          xj=molecule(j)%x       
          yj=molecule(j)%y       
          zj=molecule(j)%z       

          call distance(xi,yi,zi,xj,yj,zj,dx,dy,dz,r_2)

          coul=qi*qj/(15.d0*r_2)

          Ecoul=Ecoul+coul

        end if
      end do
    end if
  end do

  Ecoul=Ecoul*330.d0

  return

end subroutine SPLelec

subroutine force_splelec(fcoul)
!==============================

  real(8), dimension(3,N_particle) :: fcoul

  integer :: proti,protj
  integer :: parti,partj

  real(8) ::  xi,yi,zi
  real(8) ::  xj,yj,zj
  real(8) ::  dx,dy,dz
  real(8) ::  qi,qj,r2
  real(8) ::  cx,cy,cz  

  character*1 :: chi,chj
  
  fcoul(:,:)=0.d0

  do parti=1,N_particle-1  

    chi=residue(parti)%chain
    proti=residue(parti)%prot
    qi=molecule(parti)%charge
    if(qi/=0.d0) then
      xi=molecule(parti)%x
      yi=molecule(parti)%y
      zi=molecule(parti)%z
   
      do partj=parti+1,N_particle

        chj=residue(partj)%chain
        protj=residue(partj)%prot
        qj=molecule(partj)%charge
        if(qj/=0.d0.and.proti/=protj) then
!        if(qj/=0.d0.and.chi/=chj) then
          xj=molecule(partj)%x
          yj=molecule(partj)%y
          zj=molecule(partj)%z
       
          call distance(xi,yi,zi,xj,yj,zj,dx,dy,dz,r2)

          cx=(2.d0/15.d0)*qi*qj*dx/(r2**2)    
          cy=(2.d0/15.d0)*qi*qj*dy/(r2**2)    
          cz=(2.d0/15.d0)*qi*qj*dz/(r2**2)    

          fcoul(1,parti)=fcoul(1,parti)+cx
          fcoul(2,parti)=fcoul(2,parti)+cy
          fcoul(3,parti)=fcoul(3,parti)+cz

          fcoul(1,partj)=fcoul(1,partj)-cx
          fcoul(2,partj)=fcoul(2,partj)-cy
          fcoul(3,partj)=fcoul(3,partj)-cz 
        end if
      end do
    end if
  end do

  return

end subroutine force_splelec

end module born
