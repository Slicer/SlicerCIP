#ifndef __vtkSlicerAirwayInspectorModuleLogic_h
#define __vtkSlicerAirwayInspectorModuleLogic_h

// Slicer Logic includes
#include "vtkSlicerAirwayInspectorModuleLogicExport.h"
#include "vtkSlicerModuleLogic.h"

#include <vtkNew.h>
#include <vtkObjectFactory.h>

// STD includes
#include <string>

class vtkRenderWindowInteractor;
class vtkEllipseFitting;
class vtkMRMLAirwayNode;
class vtkComputeAirwayWall;
class vtkImageResliceWithPlane;

/// \ingroup Slicer_QtModules_AirwayInspector
class VTK_SLICER_AIRWAYINSPECTOR_MODULE_LOGIC_EXPORT vtkSlicerAirwayInspectorModuleLogic
  :public vtkSlicerModuleLogic
{
public:

  static vtkSlicerAirwayInspectorModuleLogic *New();
  vtkTypeMacro(vtkSlicerAirwayInspectorModuleLogic,vtkSlicerModuleLogic);
  virtual void PrintSelf(ostream& os, vtkIndent indent) override;

  vtkMRMLAirwayNode* AddAirwayNode(char *volumeNodeID,
                                   double x, double y, double z);

  void ComputeCenter(vtkMRMLAirwayNode* node);

  vtkImageData* CreateAirwaySlice(vtkMRMLAirwayNode *node);

  void ComputeAirwayWall(vtkImageData* slice, vtkMRMLAirwayNode *node, int method);

  void  AddEllipsesToImage(vtkImageData *sliceRGBImage,
                           vtkMRMLAirwayNode *node,
                           vtkImageData *rgbImage);

  void CreateColorImage(vtkImageData *resliceCT, vtkImageData *colorImage);

  vtkGetObjectMacro (Reslicer, vtkImageResliceWithPlane);
  vtkGetObjectMacro (WallSolver, vtkComputeAirwayWall);

protected:

  vtkSlicerAirwayInspectorModuleLogic();
  vtkSlicerAirwayInspectorModuleLogic(const vtkSlicerAirwayInspectorModuleLogic&); // Not implemented
  void operator=(const vtkSlicerAirwayInspectorModuleLogic&); // Not implemented

  void SetWallSolver(vtkComputeAirwayWall *ref,
                     vtkComputeAirwayWall *out);

  virtual ~vtkSlicerAirwayInspectorModuleLogic();

private:
  double SelfTuneModelSmooth[3];
  double SelfTuneModelSharp[3];
  vtkImageResliceWithPlane *Reslicer;
  vtkComputeAirwayWall     *WallSolver;
};

#endif
