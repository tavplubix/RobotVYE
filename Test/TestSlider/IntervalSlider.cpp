
//Project
#include "IntervalSlider.h"

//Qt
#include <QMouseEvent>
#include <QMimeData>
#include <QDrag>
#include <QWidgetAction>
#include <QApplication>
#include <QPixmap>
#include <QCursor>
#include <QGuiApplication>
#include <QDir>
#include <QProxyStyle>

class SliderProxy : public QProxyStyle
{
public:
  int pixelMetric ( PixelMetric metric, const QStyleOption * option = 0, const QWidget * widget = 0 ) const
  {
    switch(metric) {
    case PM_SliderThickness  : return 25;
    case PM_SliderLength     : return 25;
    default                  : return (QProxyStyle::pixelMetric(metric,option,widget));
    }
  }
};

//==================================================================================================
//					IntervalSlider Implementation
//==================================================================================================

IntervalSlider::IntervalSlider(QWidget *parent)
  : QSlider(parent)
{
  //styling
  setOrientation(Qt::Horizontal);
  setAcceptDrops(true);
  SliderProxy *aSliderProxy = new SliderProxy();
//  hard coded path to image :/ sorry
  QString path = QDir::fromNativeSeparators(ImagesPath("handle.png"));
  //setStyleSheet("QSlider::handle { image: url(" + path + "); }");
  //setStyle(aSliderProxy);
  //setStyle(QStyleFactory::create("Fusion"));
  //setting up the alternate handle
  upperHandle = new IntervalSliderHandle(this);
  addAction(new QWidgetAction(upperHandle));
  upperHandle->move(this->pos().x() + this->width()- upperHandle->width(), this->pos().y() );

  //lowerHandle = new SuperSliderHandle(this);
  //addAction(new QWidgetAction(upperHandle));
  //lowerHandle->move(this->pos().x() + this->width() - upperHandle->width(), this->pos().y());
}

void IntervalSlider::updateUpper()
{
	//QPoint posCursor(QCursor::pos());
	QPoint posParent(mapToParent(mapToGlobal(pos())));
	QPoint cursorPos = QCursor::pos();
	QPoint mappedFromGlobal = upperHandle->mapFromGlobal(cursorPos);
	QPoint mappedToParent = upperHandle->mapToParent(mappedFromGlobal);
	QPoint point(mappedToParent.x(), upperHandle->y());
	int horBuffer = (upperHandle->width());
	int maxp = pos().x() + width() - horBuffer;
	int p = mapToParent(point).x();
	bool lessThanMax = p < maxp;
	int minp = pos().x();
	bool greaterThanMin = p > pos().x();
	if (lessThanMax && greaterThanMin)
		upperHandle->move(point);
	emit upperValueChanged(upperValue());
}

void IntervalSlider::Reset()
{
	int horBuffer = (upperHandle->width());
	QPoint myPos = mapToGlobal(pos());
	int posx = myPos.x() + width() - horBuffer;
	int posy = myPos.y() - upperHandle->height();
	QPoint point(posx, posy);
	point = upperHandle->mapFromParent(point);

	upperHandle->move(point);
	upperHandle->show();
	upperHandle->raise();

}

void IntervalSlider::mouseReleaseEvent(QMouseEvent *mouseEvent)
{
	if (mouseEvent->button() == Qt::LeftButton) {
		upperHandle->show();
		upperHandle->handleActivated = false;
	}
	mouseEvent->accept();
}

int IntervalSlider::upperValue()
{
  return upperHandle->value();
}

void IntervalSlider::setUpperValue(int value)
{
  upperHandle->setValue(value);
}



//==================================================================================================
//					IntervalSliderHandle Implementation
//==================================================================================================

IntervalSliderHandle::IntervalSliderHandle(IntervalSlider *_parent)
	: QLabel(_parent)
{
	parent = _parent;
	filter = new SliderEventFilter(parent);

	//styling
	setAcceptDrops(true);
	//hard coded path to image :/ sorry
	QPixmap pix = QPixmap(ImagesPath("handle.png"));
	pix = pix.scaled(10, 22, Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
	setPixmap(pix);
}

void IntervalSliderHandle::setValue(double value)
{
	double width = parent->width();
	double position = pos().x();
	double range = parent->maximum() - parent->minimum();
	double dval = value - parent->minimum();
	int location = dval / range;
	location = location * width;
	move(y(), location);
}

int IntervalSliderHandle::value()
{
	double width = parent->width();
	double position = pos().x();
	double value = position / width;
	double range = parent->maximum() - parent->minimum();
	double dval = value * range;
	return parent->minimum() + dval;
}

void IntervalSliderHandle::mousePressEvent(QMouseEvent *mouseEvent)
{
	qGuiApp->installEventFilter(filter);
	parent->clearFocus();
}



//==================================================================================================
//					SliderEventFilter Implementation
//==================================================================================================


bool SliderEventFilter::eventFilter(QObject* obj, QEvent* event)
{
	switch (event->type()) {
	case QEvent::MouseButtonRelease:
		qGuiApp->removeEventFilter(this);
		return true;
		break;
	case QEvent::MouseMove:
		grandParent->updateUpper();
		return true;
		break;
	default:
		return QObject::eventFilter(obj, event);
	}
	return false;
}
