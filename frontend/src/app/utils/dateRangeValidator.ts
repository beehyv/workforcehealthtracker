import {AbstractControl, ValidatorFn} from '@angular/forms';

export const dateRangeValidator = (min: Date, max: Date): ValidatorFn => {
  return (control: AbstractControl) => {
    const date = new Date(control.value);
    if (isNaN(date.getTime())) {
      return {error: 'InvalidDate'};
    }
    if ( date.getTime() < min.getTime() || date.getTime() > max.getTime()) {
      return {error: 'OutOfRangeError'};
    }
    return null;
  };
};
