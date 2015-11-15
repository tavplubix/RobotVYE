#include "mainwindow.h"
#include "ui_mainwindow.h"



MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    capture(0)
{
    ui->setupUi(this);
    ui->centralWidget->setLayout(ui->gridLayout);

    connect(ui->chooseFilePushButton, &QPushButton::clicked, [&]() {
        QString filename = QFileDialog::getOpenFileName(this, "Image", "/home/tavplubix/ComputerVision");
        ui->filenameLineEdit->setText(filename);
    });

    connect(ui->setLowerLimitButton, &QPushButton::clicked, [&]() {
        qlower = QColorDialog::getColor(qlower, this);
        QString label = "R = " + QString::number(qlower.red()) + "; G = " + QString::number(qlower.green()) + "; B = " + QString::number(qlower.blue()) + ";";
        ui->lowerLimitLabel->setText(label);
        QPalette palette;
        palette.setColor(QPalette::WindowText, qlower);
        ui->lowerLimitLabel->setPalette(palette);
    });
    connect(ui->setUpperLimitButton, &QPushButton::clicked, [&]() {
        qupper = QColorDialog::getColor(qupper, this);
        QString label = "R = " + QString::number(qupper.red()) + "; G = " + QString::number(qupper.green()) + "; B = " + QString::number(qupper.blue()) + ";";
        ui->upperLimitLabel->setText(label);
        QPalette palette;
        palette.setColor(QPalette::WindowText, qupper);
        ui->upperLimitLabel->setPalette(palette);
    });

    /*connect(ui->okPushButton, &QPushButton::clicked, [&]() {
        QString path = ui->filenameLineEdit->text();
        processImage(path);
        ui->beforeLabel->setPixmap(before.scaled(800, 600, Qt::KeepAspectRatio));
        ui->maskLabel->setPixmap(mask.scaled(800, 600, Qt::KeepAspectRatio));
        ui->afterLabel->setPixmap(after.scaled(800, 600, Qt::KeepAspectRatio));
    });*/

    timer.setInterval(100);
    connect(&timer, &QTimer::timeout, [&](){
        cv::Mat frame;
        capture >> frame;
        processImage(frame);
        ui->beforeLabel->setPixmap(before.scaled(600, 600, Qt::KeepAspectRatio));
        ui->maskLabel->setPixmap(mask.scaled(600, 600, Qt::KeepAspectRatio));
        ui->afterLabel->setPixmap(after.scaled(600, 600, Qt::KeepAspectRatio));
        this->update();
    });
    timer.start();

    slider = new IntervalSlider(this);
    //slider->setSpan(0, 100);
	slider->setMinimum(0);
	slider->setValue(10);
	slider->setMaximum(255);
	slider->alt_setValue(20);
    ui->gridLayout->addWidget(slider);
    slider->show();
}

MainWindow::~MainWindow()
{
    delete ui;
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
























