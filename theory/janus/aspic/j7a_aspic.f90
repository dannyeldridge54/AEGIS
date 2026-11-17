program j7a
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use lfisr, only : lfi_x_endinf, lfi_x_trajectory, lfi_epsilon_one, lfi_epsilon_two, lfi_epsilon_three
  use sisr, only : si_x_endinf, si_x_trajectory, si_epsilon_one, si_epsilon_two, si_epsilon_three
  use nisr, only : ni_x_endinf, ni_x_trajectory, ni_epsilon_one, ni_epsilon_two, ni_epsilon_three
  use esisr, only : esi_x_endinf, esi_x_trajectory, esi_epsilon_one, esi_epsilon_two, esi_epsilon_three
  implicit none
  real(kp) :: Ns(2) = (/50._kp, 60._kp/), x, xe, e(3), t0, t1, p
  integer :: i, j, k, rep
  character(len=8) :: nm
  do i = 1, 7
    do j = 1, 2
      call cpu_time(t0)
      do rep = 1, 1000
      select case (i)
      case (1,2,3)
        p = merge(2._kp, merge(4._kp, 2._kp/3._kp, i==2), i==1)
        xe = lfi_x_endinf(p); x = lfi_x_trajectory(-Ns(j), xe, p)
        e = (/lfi_epsilon_one(x,p), lfi_epsilon_two(x,p), lfi_epsilon_three(x,p)/)
      case (4)
        p = 0._kp; xe = si_x_endinf(); x = si_x_trajectory(-Ns(j), xe)
        e = (/si_epsilon_one(x), si_epsilon_two(x), si_epsilon_three(x)/)
      case (5,6)
        p = merge(5._kp, 10._kp, i==5)
        xe = ni_x_endinf(p); x = ni_x_trajectory(-Ns(j), xe, p)
        e = (/ni_epsilon_one(x,p), ni_epsilon_two(x,p), ni_epsilon_three(x,p)/)
      case (7)
        p = 1._kp; xe = esi_x_endinf(p); x = esi_x_trajectory(-Ns(j), xe, p)
        e = (/esi_epsilon_one(x,p), esi_epsilon_two(x,p), esi_epsilon_three(x,p)/)
      end select
      end do
      call cpu_time(t1)
      write(*,'(I2,1X,F8.4,1X,F5.1,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES12.4)') i, p, Ns(j), x, &
        scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), xe, (t1-t0)/1000._kp
    end do
  end do
end program j7a
