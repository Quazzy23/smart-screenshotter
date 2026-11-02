import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QRect, QPoint, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QGuiApplication, QColor, QPainter, QPen
import keyboard

# ==========================================
# НАСТРОЙКИ ДЛЯ ТЕСТА (МЕНЯЙ ЗДЕСЬ)
# ==========================================
DARK_COLOR = QColor(0, 0, 0, 120) # Цвет и прозрачность затемнения (R, G, B, Alpha)
FADE_DURATION = 100               # Время появления и затухания (в миллисекундах)

# Клавиши (можно писать 'print screen', 'alt+print screen', 'ctrl+shift+s' и т.д.)
HOTKEY_FULLSCREEN = 'print screen'       # Клавиша для обычного скриншота
HOTKEY_AREA = 'alt+print screen'         # Клавиша для выделения области
# ==========================================

# --- КЛАСС ДЛЯ ВСПЫШКИ (Обычный Print Screen) ---
class FlashOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        screen = QGuiApplication.primaryScreen()
        self.setGeometry(screen.geometry())

        self.anim_in = QPropertyAnimation(self, b"windowOpacity")
        self.anim_in.setDuration(FADE_DURATION)
        self.anim_in.setStartValue(0.0)
        self.anim_in.setEndValue(1.0)
        self.anim_in.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.anim_out = QPropertyAnimation(self, b"windowOpacity")
        self.anim_out.setDuration(FADE_DURATION)
        self.anim_out.setStartValue(1.0)
        self.anim_out.setEndValue(0.0)
        self.anim_out.setEasingCurve(QEasingCurve.Type.InQuad)
        self.anim_out.finished.connect(self.hide)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), DARK_COLOR)

    def flash(self):
        self.setWindowOpacity(0.0)
        self.showFullScreen()
        
        self.anim_in.stop()
        self.anim_in.start()
        
        try:
            self.anim_in.finished.disconnect(self.start_fade_out)
        except TypeError:
            pass
            
        self.anim_in.finished.connect(self.start_fade_out)
        
    def start_fade_out(self):
        self.anim_out.stop()
        self.anim_out.start()

# --- КЛАСС ДЛЯ ВЫДЕЛЕНИЯ ОБЛАСТИ ---
class SnippingOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.CrossCursor)
        
        self.original_pixmap = None
        self.dark_pixmap = None
        self.origin = QPoint()
        self.current_pos = QPoint()
        self.is_drawing = False
        self.needs_redraw = False

        self.render_timer = QTimer(self)
        self.render_timer.timeout.connect(self.smooth_update)
        self.render_timer.start(8)

        self.anim_in = QPropertyAnimation(self, b"windowOpacity")
        self.anim_in.setDuration(FADE_DURATION)
        self.anim_in.setStartValue(0.0)
        self.anim_in.setEndValue(1.0)
        
        self.anim_out = QPropertyAnimation(self, b"windowOpacity")
        self.anim_out.setDuration(FADE_DURATION)
        self.anim_out.setStartValue(1.0)
        self.anim_out.setEndValue(0.0)
        self.anim_out.finished.connect(self.hide)

    def take_screenshot(self):
        screen = QGuiApplication.primaryScreen()
        self.setGeometry(screen.geometry())
        self.original_pixmap = screen.grabWindow(0)
        self.dark_pixmap = self.original_pixmap.copy()
        painter = QPainter(self.dark_pixmap)
        painter.fillRect(self.dark_pixmap.rect(), DARK_COLOR)
        painter.end()

    def show_animated(self):
        self.is_drawing = False
        self.origin = QPoint()
        self.current_pos = QPoint()
        
        self.take_screenshot()
        self.update()
        
        self.setWindowOpacity(0.0)
        self.showFullScreen()
        self.anim_in.stop()
        self.anim_in.start()

    def start_fade_out(self):
        self.anim_out.stop()
        self.anim_out.start()

    def smooth_update(self):
        if self.needs_redraw:
            self.needs_redraw = False
            self.update()

    def paintEvent(self, event):
        if not self.dark_pixmap:
            return

        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.dark_pixmap)
        
        if self.is_drawing:
            rect = QRect(self.origin, self.current_pos).normalized()
            
            if rect.width() > 20 and rect.height() > 20:
                painter.drawPixmap(rect, self.original_pixmap, rect)
            
            pen = QPen(Qt.GlobalColor.white, 1, Qt.PenStyle.CustomDashLine)
            pen.setDashPattern([4, 4])
            pen.setCapStyle(Qt.PenCapStyle.FlatCap)
            painter.setPen(pen)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
            
            x1, y1 = rect.left(), rect.top()
            x2, y2 = rect.right(), rect.bottom()
            
            painter.drawLine(x1, y1, x2, y1)
            painter.drawLine(x2, y1, x2, y2)
            painter.drawLine(x1, y2, x2, y2)
            painter.drawLine(x1, y1, x1, y2)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.origin = event.pos()
            self.current_pos = event.pos()
            self.is_drawing = True
            self.needs_redraw = True

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.current_pos = event.pos()
            self.needs_redraw = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_drawing:
            self.is_drawing = False
            rect = QRect(self.origin, self.current_pos).normalized()
            print(f"Выделена область: {rect.x()}, {rect.y()}, {rect.width()}, {rect.height()}")
            self.start_fade_out()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.is_drawing = False
            self.start_fade_out()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    flash_overlay = FlashOverlay()
    snip_overlay = SnippingOverlay()

    trigger_flash = [False]
    trigger_snip = [False]

    # Назначаем хоткеи из глобальных переменных
    keyboard.add_hotkey(HOTKEY_FULLSCREEN, lambda: trigger_flash.__setitem__(0, True))
    keyboard.add_hotkey(HOTKEY_AREA, lambda: trigger_snip.__setitem__(0, True))

    def check_triggers():
        if trigger_flash[0]:
            trigger_flash[0] = False
            flash_overlay.flash()
            
        if trigger_snip[0]:
            trigger_snip[0] = False
            snip_overlay.show_animated()
            
        QTimer.singleShot(50, check_triggers)

    check_triggers()
    print(f"Запущено! {HOTKEY_FULLSCREEN} = вспышка. {HOTKEY_AREA} = выделение.")
    sys.exit(app.exec())