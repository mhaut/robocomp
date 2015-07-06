//******************************************************************
// 
//  Generated by IDSL to IDL Translator
//  
//  File name: BodyInverseKinematics.idl
//  Source: BodyInverseKinematics.idsl
//  
//******************************************************************   
#ifndef ROBOCOMPINVERSEKINEMATICS_ICE
#define ROBOCOMPINVERSEKINEMATICS_ICE

module RoboCompInverseKinematics{
	exception IKException{string text;};
	["cpp:comparable"]
	struct Pose6D{
		float x;
		float y;
		float z;
		float rx;
		float ry;
		float rz;
	};
	["cpp:comparable"]
	struct WeightVector{
		float x;
		float y;
		float z;
		float rx;
		float ry;
		float rz;
	};
	["cpp:comparable"]
	struct Axis{
		float x;
		float y;
		float z;
	};
	["cpp:comparable"]
	struct Motor{
		string name;
		float angle;
	};
	sequence<Motor> MotorList;
	["cpp:comparable"]
	struct TargetState{
		bool finish;
		int elapsedTime;
		int estimatedEndTime;
		float errorT;
		float errorR;
		MotorList motors;
	};

	interface InverseKinematics
	{
		TargetState getTargetState(string bodyPart, int targetID);
		int setTargetPose6D(string bodyPart, Pose6D target, WeightVector weights) throws IKException;
		int setTargetAlignaxis(string bodyPart, Pose6D target, Axis ax) throws IKException;
		int setTargetAdvanceAxis(string bodyPart, Axis ax, float dist) throws IKException;
		bool getPartState(string bodyPart);

		void goHome(string bodyPart) throws IKException;
		void stop(string bodyPart);
	};
};
  
#endif