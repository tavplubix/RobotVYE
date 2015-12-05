#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QPixmap>
#include <QPainter>
#include <QFont>




MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    capture(0),
	qlower(Qt::black),
	qupper(Qt::white)
{
    ui->setupUi(this);
    ui->centralWidget->setLayout(ui->gridLayout);

	rSlider = new MyIntervalSlider(this);
	gSlider = new MyIntervalSlider(this);
	bSlider = new MyIntervalSlider(this);

	ui->formLayout_2->addRow("Red:", rSlider);
	ui->formLayout_2->addRow("Green:", gSlider);
	ui->formLayout_2->addRow("Blue:", bSlider);

	setupFormLayout(ui->formLayout_3);

	setupSliders();

	connect(ui->showOriginalCheckBox, &QCheckBox::stateChanged, this, [&](int state) {
		if (state == Qt::Unchecked) ui->beforeLabel->hide();
		else ui->beforeLabel->show();
	});
	connect(ui->showMaskCheckBox, &QCheckBox::stateChanged, this, [&](int state) {
		if (state == Qt::Unchecked) ui->maskLabel->hide();
		else ui->maskLabel->show();
	});
	connect(ui->showResultCheckBox, &QCheckBox::stateChanged, this, [&](int state) {
		if (state == Qt::Unchecked) ui->afterLabel->hide();
		else ui->afterLabel->show();
	});

    timer.setInterval(100);
    connect(&timer, &QTimer::timeout, [&](){
        cv::Mat frame;
        capture >> frame;
        processImage(frame);
		int picturesChecked = ui->showOriginalCheckBox->isChecked() + ui->showMaskCheckBox->isChecked() + ui->showResultCheckBox->isChecked();
		if (picturesChecked == 0) return;
		int width = (this->width() - 30) / picturesChecked;
        ui->beforeLabel->setPixmap(before.scaled(width, 1080, Qt::KeepAspectRatio));
        ui->maskLabel->setPixmap(mask.scaled(width, 1080, Qt::KeepAspectRatio));
        ui->afterLabel->setPixmap(after.scaled(width, 1080, Qt::KeepAspectRatio));
        this->update();
    });
    timer.start();

	

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::setupSlider(MyIntervalSlider* &slider)
{
	//slider->setSpan(0, 100);
	slider->setMinimum(0);
	slider->setMaximum(255);
	slider->setMinimumWidth(255);
	slider->setMinimumHeight(26);
	slider->setLowerValue(0);
	slider->setUpperValue(255);
	slider->show();
}

void MainWindow::setupSliders()
{
	connect(rSlider, &MyIntervalSlider::valueChanged, this, [&](int val) {
		qlower.setRed(rSlider->lowerValue());
		qupper.setRed(rSlider->upperValue());
		drawColorLabel(rlabel, QColor(qlower.red(), 0, 0), QColor(qupper.red(), 0, 0));
		drawColorLabel(label, qlower, qupper);
	});
	connect(gSlider, &MyIntervalSlider::valueChanged, this, [&](int val) {
		qlower.setGreen(gSlider->lowerValue());
		qupper.setGreen(gSlider->upperValue());
		drawColorLabel(glabel, QColor(0, qlower.green(), 0), QColor(0, qupper.green(), 0));
		drawColorLabel(label, qlower, qupper);
	});
	connect(bSlider, &MyIntervalSlider::valueChanged, this, [&](int val) {
		qlower.setBlue(bSlider->lowerValue());
		qupper.setBlue(bSlider->upperValue());
		drawColorLabel(blabel, QColor(0, 0, qlower.blue()), QColor(0, 0, qupper.blue()));
		drawColorLabel(label, qlower, qupper);
	});
	setupSlider(rSlider);
	setupSlider(gSlider);
	setupSlider(bSlider);
}

void MainWindow::setupFormLayout(QFormLayout *layout)
{
	rlabel = new QLabel(this);
	layout->addRow("Red:", rlabel);

	glabel = new QLabel(this);
	layout->addRow("Green:", glabel);

	blabel = new QLabel(this);
	layout->addRow("Blue:", blabel);

	label = new QLabel(this);
	layout->addRow("Color:", label);
	
}

void MainWindow::drawColorLabel(QLabel* pd, const QColor &lc, const QColor& uc)
{
	QPixmap pixmap(102, 26);
	QPainter painter(&pixmap);
	//QRect lowerText(0, 0, 40, 30);
	//QRect upperText(90, 0, 40, 30);
	QRect lowerColor(0, 0, 50, 25);
	QRect upperColor(50, 0, 50, 25);

	QFont font("Times", 11);
	painter.setFont(font);

	painter.setPen(Qt::black);
	painter.setBrush(lc);
	painter.drawRect(lowerColor);
	int lgray = lc.red() + lc.green() + lc.blue();
	painter.setPen(invert(lc));
	painter.drawText(lowerColor.translated(8, 2), QString::number(lgray));

	painter.setPen(Qt::black);
	painter.setBrush(uc);
	painter.drawRect(upperColor);
	int ugray = uc.red() + uc.green() + uc.blue();
	painter.setPen(invert(uc));
	painter.drawText(upperColor.translated(8, 2), QString::number(ugray));

	pd->setPixmap(pixmap);
}

void MainWindow::processImage(cv::Mat cvimage/*const QString &filename*/)
{
    //cv::Mat cvimage;
    //cvimage = cv::imread(filename.toLocal8Bit().data(), CV_LOAD_IMAGE_COLOR);
    cv::Scalar lower = cv::Scalar(qlower.blue(), qlower.green(), qlower.red());
    cv::Scalar upper = cv::Scalar(qupper.blue(), qupper.green(), qupper.red());
    cv::Mat mask(cvimage.rows, cvimage.cols, CV_8UC3);
    cv::inRange(cvimage, lower, upper, mask);
    cv::Mat result(cvimage.rows, cvimage.cols, CV_8UC3);
    cv::bitwise_and(cvimage, cvimage, result, mask);
    before = cvMatToQImage(cvimage);
    this->mask = cvMatToQImage(mask);
    after = cvMatToQImage(result);
}

QPixmap MainWindow::cvMatToQImage(const cv::Mat &cvm)
{
    cv::Mat _tmp;
    switch (cvm.type()) {
            case CV_8UC1:
                cvtColor(cvm, _tmp, CV_GRAY2RGB);
                break;
            case CV_8UC3:
                cvtColor(cvm, _tmp, CV_BGR2RGB);
                break;
            default:
                throw 0;
    }
    //cv::cvtColor(cvm, _tmp, CV_BGR2RGB);
    assert(_tmp.isContinuous());
    qDebug() << _tmp.cols << "    " << _tmp.rows << "    ";
    uchar* d = _tmp.data;
    QPixmap pm = QPixmap::fromImage(QImage(d, _tmp.cols, _tmp.rows, _tmp.cols*3, QImage::Format_RGB888));   //CRUTCH
    return pm;
}

QColor MainWindow::invert(const QColor& color)
{
	QColor inverted;
	inverted.setRed(255 - color.red());
	inverted.setGreen(255 - color.green());
	inverted.setBlue(255 - color.blue());
	return inverted;
}























