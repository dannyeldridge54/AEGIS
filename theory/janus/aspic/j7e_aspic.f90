program j7e
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use wrisr, only : wri_x_endinf, wri_x_trajectory, wri_epsilon_one, wri_epsilon_two, wri_epsilon_three
  use kmiiisr, only : kmiii_x_endinf, kmiii_x_trajectory, kmiii_epsilon_one, kmiii_epsilon_two, kmiii_epsilon_three
  use cnaisr, only : cnai_x_endinf, cnai_x_trajectory, cnai_epsilon_one, cnai_epsilon_two, cnai_epsilon_three
  use cnbisr, only : cnbi_x_endinf, cnbi_x_trajectory, cnbi_epsilon_one, cnbi_epsilon_two, cnbi_epsilon_three
  use sbkisr, only : sbki_x_endinf, sbki_x_trajectory, sbki_epsilon_one, sbki_epsilon_two, sbki_epsilon_three
  use lfisr, only : lfi_x_endinf, lfi_x_trajectory, lfi_epsilon_one, lfi_epsilon_two, lfi_epsilon_three
  implicit none
  real(kp) :: Ns(2) = (/50._kp, 60._kp/), x, xe, e(3)
  integer :: i, j
  do i = 1, 6
  do j = 1, 2
  select case (i)
  case (1); xe = wri_x_endinf(10._kp); x = wri_x_trajectory(-Ns(j), xe, 10._kp)
    e = (/wri_epsilon_one(x,10._kp), wri_epsilon_two(x,10._kp), wri_epsilon_three(x,10._kp)/)
  case (2); xe = kmiii_x_endinf(1._kp,1._kp); x = kmiii_x_trajectory(-Ns(j), xe, 1._kp, 1._kp)
    e = (/kmiii_epsilon_one(x,1._kp,1._kp), kmiii_epsilon_two(x,1._kp,1._kp), kmiii_epsilon_three(x,1._kp,1._kp)/)
  case (3); xe = cnai_x_endinf(0.1_kp); x = cnai_x_trajectory(-Ns(j), xe, 0.1_kp)
    e = (/cnai_epsilon_one(x,0.1_kp), cnai_epsilon_two(x,0.1_kp), cnai_epsilon_three(x,0.1_kp)/)
  case (4); xe = cnbi_x_endinf(0.1_kp); x = cnbi_x_trajectory(-Ns(j), xe, 0.1_kp)
    e = (/cnbi_epsilon_one(x,0.1_kp), cnbi_epsilon_two(x,0.1_kp), cnbi_epsilon_three(x,0.1_kp)/)
  case (5); xe = sbki_x_endinf(-0.01_kp); x = sbki_x_trajectory(-Ns(j), xe, -0.01_kp)
    e = (/sbki_epsilon_one(x,-0.01_kp), sbki_epsilon_two(x,-0.01_kp), sbki_epsilon_three(x,-0.01_kp)/)
  case (6); xe = lfi_x_endinf(6._kp); x = lfi_x_trajectory(-Ns(j), xe, 6._kp)
    e = (/lfi_epsilon_one(x,6._kp), lfi_epsilon_two(x,6._kp), lfi_epsilon_three(x,6._kp)/)
  end select
  write(*,'(I3,1X,F5.1,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14)') i, Ns(j), x, &
     scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), xe
  end do
  end do
end program j7e
