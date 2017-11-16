! Subroutine saddle_converge
!
! This subroutine bring the configuration to a saddle point. It does that
! by first pushing the configuration outside of the harmonic well, using
! the initial direction selected in find_saddle. Once outside the harmonic
! well, as defined by the appearance of a negative eigenvalue (or
! reasonnable size) the configuration follows the direction corresponding
! to this eigenvalue until the force components parallel and perpdendicular
! to the eigendirection become close to zero.
!
!  Normand Mousseau, June 2001
!
! Integration dans programme docking, 2005
module saddle_converge_pro

  use particles
  use run_parameter
  use energa
!  use eigen90
  use lanczos_pro
 
  implicit none

  contains

 subroutine saddle_converge(ret,saddle_energy,fpar,fperp)
!========================================================

  integer, intent(out) :: ret
  real(8), intent(out) :: saddle_energy, fpar, fperp

  integer :: k, kter, iter, iperp, k_rejected
  integer :: itry,new_projection,maxvec
  real(8) :: fdotinit, fperp2, current_fperp
  real(8) :: step
  real(8) :: one = 1.0d0
  real(8) :: dr,dt
  real(8) :: current_energy,Elj,Eelec
  real(8), dimension(Nvar) :: force,grad  
  real(8), dimension(Nvar) :: perp_force, posb, forceb, perp_forceb  
  real(8), dimension(Nvar) :: initial_directionb 
  real(8), dimension(Nvar) :: projection
  real(8), dimension(6) :: scal,dlig
 
!  real(8), dimension(Nvar*(Nvar+1)/2) :: Hessian
!  real(8), dimension(Nvar*Nvar) :: evectors                            

 scal(1:3)=1.d0
 scal(4:6)=15.d0 

  eigenvalue=0.0d0
!  Hessian(:)=0.d0
  
  do kter=1,50  !! 200 for 
     
    call energy(Lig_position,current_energy,Elj,Eelec,grad)
    force(:)=-grad(:)   
     evalf_number = evalf_number + 1
     ! We now project the direction of the initial displacement from the
     ! minimum onto the strong force direction, then we remove the projection 
     ! from the initial direction and obtain the new initial direction. The 
     ! reason is that the activated events don't involve an appreciable 
     ! displacement along the rigid directions. Then we do energy minimization 
     ! in the direction perpendicular to the new initial direction 
     
    fdotinit=0.0d0
    fdotinit=dot_product(force,initial_direction)

    perp_force(:)=force(:)-fdotinit*initial_direction(:)
     
    step=0.30d0*INCREMENT !! 0.10-0.30 IDRIS 0.25 
     
    k=0
    k_rejected=0
     
! We relax perpendicularly using a simple variable-step steepest descent 
    do 
      posb(:)=Lig_position(:)+step*perp_force(:)
        
      call energy(posb,total_energy,Elj,Eelec,grad)
      forceb=-grad 
      evalf_number = evalf_number + 1
        
      fdotinit=0.0d0
      fdotinit=dot_product(forceb,initial_direction)
        
      perp_forceb(:)=forceb(:)-fdotinit*initial_direction(:)
        
      fperp2=0.0d0
      fperp2=dot_product(perp_forceb,perp_forceb)
      fperp =sqrt(fperp2)
        
      if(total_energy<current_energy ) then
!        initial_direction = initial_directionb
        Lig_position=posb
        force=forceb
        perp_force=perp_forceb
        step=1.2*step
        current_energy=total_energy
        k_rejected=0
        k=k+1
      else
        step = 0.6 * step
        k_rejected = k_rejected + 1
      endif
        
      if(fperp2 < FTHRESH2 .or. k > MAXIPERP .or. k_rejected > 5) exit
    end do
     
! We now move the configuration along the initial direction and check the lowest
! eigendirection
     
    Lig_position=Lig_position+5.0*INCREMENT*initial_direction*scal  ! 10 IDRIS 

! We start checking of negative eigenvalues after a few steps or at every step
    if( kter>= 1 ) then 
        maxvec=Nvar
        new_projection=0
        call lanczos(maxvec,new_projection,projection)
!      call eigen(Hessian,evectors)
!      eigenvalue=Hessian(1)
!      projection=evectors(1:Nvar) 
    endif
    current_energy = total_energy ! As computed in lanczos routine

    dlig(:)=Lig_position(:)-Lig_ref(:)
    dr=sqrt(dlig(1)**2+dlig(2)**2+dlig(3)**2)
    dt=sqrt(dlig(4)**2+dlig(5)**2+dlig(6)**2)

    if(mod(kter,1)==0) then
      write(6,"(' kt:',i4,' k:',i2,' En:',f8.4,' eval:',f10.6,' fpar:',&
            f9.4,' fperp:',f9.4,' step:',f10.7,' dr:',f8.4,' dt:',f8.4)")  &
            kter,k,total_energy,eigenvalue,fdotinit,fperp,step,dr,dt
    end if
     
    if(eigenvalue < EIGEN_THRESH .and. kter > 4) exit
  end do

! The configuration is now out of the harmonic well, we can now bring
! it to the saddle point. Again, we split the move into a parallel and 
! perpendicular contribution.
  
! First, we must now orient the direction of the eigenvector corresponding to the
! negative eigendirection (called projection) such that it points away from minimum. 
  
  call energy(Lig_position,current_energy,Elj,Eelec,grad) 
  force=-grad 
  evalf_number = evalf_number + 1
  
  fpar=0.0d0
  fpar=dot_product(force,projection)
  
  if(fpar > 0.0d0 ) then
     projection = -projection
  end if

  !  pos = pos + 10.0d0 * INCREMENT * projection   
  Lig_position = Lig_position +  30.0d0 * INCREMENT * projection 
! parameters artoctamer and duvernay, Wei
  
  call energy(Lig_position,current_energy,Elj,Eelec,grad)
  force=-grad 
  evalf_number = evalf_number + 1
  
  fpar=0.0d0
  fpar=dot_product(force,projection)  
  
  perp_force(:)=force(:)-fpar*projection(:)  ! Vectorial force
  
  fperp2=0.0d0
  fperp2=dot_product(perp_force,perp_force)
  current_fperp = sqrt(fperp2)
  
  do iter=1,MAXITERART 
     
    step=0.05d0*INCREMENT 
     
    itry = 0
    iperp = 0
     
! The following loop is on the perpendicular direction, again using a 
! variable-step steepest descent
     
    do  
      posb = Lig_position + step * perp_force
      call energy(posb,total_energy,Elj,Eelec,grad)
      forceb=-grad 
      evalf_number = evalf_number + 1
        
      fpar= 0.0d0
      fpar=dot_product(forceb,projection)
      perp_force= forceb-fpar*projection  ! Vectorial force
        
      fperp2 = 0.0d0
      fperp2=dot_product(perp_force,perp_force)
      fperp = sqrt(fperp2)
        
      if(total_energy < current_energy ) then
 !      if(fperp < current_fperp ) then
        Lig_position = posb
        force = forceb
        step = 1.2 * step
        current_energy=total_energy
        current_fperp=fperp
        iperp=iperp+1
      else
         step = 0.6 * step
      endif
      itry = itry + 1
        
      if(fperp2 < FTHRESH2 .or. iperp > (iter - 10)  .or. iperp > 10 .or.  itry > 15) exit
        ! if(fperp2 < FTHRESH2 .or. iperp > 20 .or.  itry > 10) exit
    end do
      
    new_projection = 1    ! We use previously computed lowest direction as seed
    call lanczos(maxvec,new_projection,projection)
!    call eigen(Hessian,evectors)
!    eigenvalue=Hessian(1)
!    projection=evectors(1:Nvar) 
     
    current_energy = total_energy ! As computed in lanczos routine
     
    fpar= 0.d0
    fpar=dot_product(force,projection)
     
! We now move the configuration along the eigendirection corresponding
! to the lowest eigenvalue
     
    if(abs(fpar)>0.5) then ! 0.5
      Lig_position=Lig_position-sign(one,fpar)*15.d0*INCREMENT*projection/sqrt(1.d0*iter) ! 15.0
    else
      Lig_position=Lig_position-sign(one,fpar)*5.0d0*INCREMENT*projection/sqrt(1.d0*iter) 
    endif
     
    call energy(Lig_position,total_energy,Elj,Eelec,grad)
    force=-grad
    evalf_number = evalf_number + 1
     
    fpar= 0.0d0
    fpar=dot_product(force,projection)

    perp_force=force-fpar*projection  ! Vectorial force
    fperp2 = 0.0d0
    fperp2=dot_product(perp_force,perp_force)
    fperp = sqrt(fperp2)
    current_fperp = fperp 

    dlig(:)=Lig_position(:)-Lig_ref(:)
    dr=sqrt(dlig(1)**2+dlig(2)**2+dlig(3)**2)
    dt=sqrt(dlig(4)**2+dlig(5)**2+dlig(6)**2)
          
    if( mod(iter,1) == 0 ) then
      write(6,"(' ','it:',i4,' ip:',i4,' en:',f10.4,' fpar:',f9.4,' fperp:',&
            f9.4, ' e-val:', f12.6,' dr:',f8.4,'  dt:',f8.4)") &
            iter, iperp, total_energy, fpar, fperp, eigenvalue,dr,dt


     !  write(*,"(' ','bond_en: ',f10.4,' angle_en: ', f10.4,' torsion_en: ', &
     ! & f8.4,' vdw_en: ',f8.4,' hydro_en: ',f9.4,' nbnd_en: ',f10.4,  &
     ! & ' hb_en: ',f9.4, &
     ! & )") ener(1),ener(2),ener(3),ener(4),ener(5),ener(6),ener(7)

    endif

    saddle_energy = total_energy
    current_energy = total_energy
      
    if ( (abs(fpar)+fperp)<EXITTHRESH)  then  !! 1.250 
      ret = 20000 + iter
      exit
    else if ( (abs(fpar)<0.05*EXITTHRESH) .and. (fperp<0.9*EXITTHRESH) ) then !! 1.15
      ret = 10000 + iter
      exit
    else if (eigenvalue>0.0) then
      ret = 60000 + iter
      exit
    endif

  end do
  
  return

end subroutine saddle_converge

end module saddle_converge_pro
