#include "wled.h"
/*
 * Register your v2 usermods here!
 *   (Please let me know if you created a WLED usermod!)
 */

#ifdef USERMOD_MATRIX_DISPLAY
  #include "../usermods/matrix_display/usermod_matrix_display.h"
  UsermodMatrixDisplay usermodMatrixDisplay;
  REGISTER_USERMOD(usermodMatrixDisplay);
#endif
