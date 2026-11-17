program j7d
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use tisr, only : ti_x_endinf, ti_x_trajectory, ti_epsilon_one, ti_epsilon_two, ti_epsilon_three
  use psnisr, only : psni_x_endinf, psni_x_trajectory, psni_epsilon_one, psni_epsilon_two, psni_epsilon_three
  use sfisr, only : sfi_x_endinf, sfi_x_trajectory, sfi_epsilon_one, sfi_epsilon_two, sfi_epsilon_three
  implicit none
  real(kp) :: Ns(2) = (/50._kp, 60._kp/), x, xe, e(3), a, b
  integer :: i, j
  do i = 1, 5
  do j = 1, 2
  select case (i)
  case (1,2)
    a = merge(0.1_kp, 0.2_kp, i==1); b = merge(10._kp, 8._kp, i==1)
    xe = ti_x_endinf(a,b); x = ti_x_trajectory(-Ns(j), xe, a, b)
    e = (/ti_epsilon_one(x,a,b), ti_epsilon_two(x,a,b), ti_epsilon_three(x,a,b)/)
  case (3)
    a = 1e-3_kp; b = 5._kp; xe = psni_x_endinf(a,b); x = psni_x_trajectory(-Ns(j), xe, a, b)
    e = (/psni_epsilon_one(x,a,b), psni_epsilon_two(x,a,b), psni_epsilon_three(x,a,b)/)
  case (4,5)
    a = merge(4._kp, 2._kp, i==4); b = merge(15._kp, 10._kp, i==4)
    xe = sfi_x_endinf(a,b); x = sfi_x_trajectory(-Ns(j), xe, a, b)
    e = (/sfi_epsilon_one(x,a,b), sfi_epsilon_two(x,a,b), sfi_epsilon_three(x,a,b)/)
  end select
  write(*,'(I3,1X,F5.1,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14)') i, Ns(j), x, &
     scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), xe
  end do
  end do
end program j7d
