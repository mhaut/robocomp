#pragma once

#include "cameraI.h"
#include "differentialrobotI.h"
#include "imuI.h"
#include "jointmotorI.h"
#include "laserI.h"
#include "rgbdI.h"

#include <CommonHead.h>

// Namespaces
// using namespace std;
// using namespace RoboCompCamera;
// using namespace RoboCompCommonHead;
// using namespace RoboCompDifferentialRobot;
// using namespace RoboCompLaser;
// using namespace RoboCompIMU;

/** XXXServer **/
/** XXXServer **/
/** XXXServer **/
class JointMotorServer
{
public:
	JointMotorServer(Ice::CommunicatorPtr communicator, SpecificWorker *worker_, uint32_t _port);
	void add(InnerModelJoint *joint);
	void remove(InnerModelJoint *joint);
	bool empty();
	void shutdown();

	uint32_t port;
	Ice::CommunicatorPtr comm;
	Ice::ObjectAdapterPtr adapter;
	JointMotorI *interface;
	std::vector<InnerModelJoint *> joints;
	SpecificWorker *worker;
};


class LaserServer
{
public:
	LaserServer(Ice::CommunicatorPtr communicator, SpecificWorker *worker, uint32_t _port);
	void add(InnerModelLaser *laser);

	uint32_t port;
	Ice::ObjectAdapterPtr adapter;
	LaserI *interface;
	std::vector<InnerModelLaser *> lasers;
};


class RGBDServer
{
public:
	RGBDServer(Ice::CommunicatorPtr communicator, SpecificWorker *worker, uint32_t _port);
	void add(InnerModelRGBD *rgbd);

	uint32_t port;
	Ice::ObjectAdapterPtr adapter;
	RGBDI *interface;
	std::vector<InnerModelRGBD *> rgbds;
};


class IMUServer
{
public:
	IMUServer(Ice::CommunicatorPtr communicator, SpecificWorker *worker, uint32_t _port);
	void add(InnerModelIMU *imu);

	uint32_t port;
	Ice::ObjectAdapterPtr adapter;
	IMUI *interface;
	std::vector<InnerModelIMU *> imus;
};


class DifferentialRobotServer
{
public:
	DifferentialRobotServer(Ice::CommunicatorPtr communicator, SpecificWorker *worker, uint32_t _port);
	void add(InnerModelDifferentialRobot *differentialrobot);

	uint32_t port;
	Ice::ObjectAdapterPtr adapter;
	DifferentialRobotI *interface;
	std::vector<InnerModelDifferentialRobot *> differentialrobots;
};