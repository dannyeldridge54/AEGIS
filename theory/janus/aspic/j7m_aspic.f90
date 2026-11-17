program j7m
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use tisr, only : ti_x_endinf, ti_x_trajectory, ti_epsilon_one, ti_epsilon_two, ti_epsilon_three
  use psnisr, only : psni_x_endinf, psni_x_trajectory, psni_epsilon_one, psni_epsilon_two, psni_epsilon_three
  use sfisr, only : sfi_x_endinf, sfi_x_trajectory, sfi_epsilon_one, sfi_epsilon_two, sfi_epsilon_three
  implicit none
  real(kp) :: Ns(2) = (/50._kp, 60._kp/), x, xe, e(3)
  real(kp) :: A(12) = (/0.05_kp,0.05_kp,0.15_kp,0.15_kp,0.3_kp,0.3_kp, 1e-4_kp,1e-2_kp,1e-3_kp, 1._kp,3._kp,3._kp/)
  real(kp) :: B(12) = (/6._kp,12._kp,6._kp,12._kp,6._kp,12._kp, 5._kp,5._kp,10._kp, 8._kp,8._kp,20._kp/)
  integer :: i, j
  do i = 1, 12
  do j = 1, 2
  if (i <= 6) then
    xe = ti_x_endinf(A(i),B(i)); x = ti_x_trajectory(-Ns(j), xe, A(i), B(i))
    e = (/ti_epsilon_one(x,A(i),B(i)), ti_epsilon_two(x,A(i),B(i)), ti_epsilon_three(x,A(i),B(i))/)
  else if (i <= 9) then
    xe = psni_x_endinf(A(i),B(i)); x = psni_x_trajectory(-Ns(j), xe, A(i), B(i))
    e = (/psni_epsilon_one(x,A(i),B(i)), psni_epsilon_two(x,A(i),B(i)), psni_epsilon_three(x,A(i),B(i))/)
  else
    xe = sfi_x_endinf(A(i),B(i)); x = sfi_x_trajectory(-Ns(j), xe, A(i), B(i))
    e = (/sfi_epsilon_one(x,A(i),B(i)), sfi_epsilon_two(x,A(i),B(i)), sfi_epsilon_three(x,A(i),B(i))/)
  end if
  write(*,'(I3,1X,F5.1,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14)') i, Ns(j), x, &
     scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), xe
  end do
  end do
end program j7m
