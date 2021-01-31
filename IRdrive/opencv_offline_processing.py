import numpy as np
import cv2

# cap = cv2.VideoCapture('MARKfun\IRdrive\data\ir_drive_camcal.avi')
cap = cv2.VideoCapture('data\ir_drive_nowhitecal.avi')
out = cv2.VideoWriter('drive.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, (240,320))

blackThreshold = 60

while(cap.isOpened()):
    ret, frame = cap.read()
    # print("ret "+str(ret)+" type "+str(type(frame)))
    if not ret or not isinstance(frame,np.ndarray):
        break
    frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
    h,w,_= frame.shape    
    img2gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # img = cv2.medianBlur(img2gray,5)
    # img = cv2.GaussianBlur(img2gray,(15,15),0)
    mmatch = np.zeros((h,256,3))
    # histogram of grey shades
    shades, bin_edges = np.histogram(img2gray, bins=np.arange(256),density=True)
    shademax = shades.max()
    shades = 100 - shades * 100 / shademax;
    # Count black pixels
    ret, mask = cv2.threshold(img2gray, blackThreshold, 255, cv2.THRESH_BINARY_INV)
    maskview = mask.sum(axis=0)
    masksum = mask.sum(axis=0)
    # Matlab type position, get two thirds of maximum to bin
    masksum[masksum < masksum.max()*(2/3)] = 0
    ind = masksum > masksum.max()*(2/3)
    maskpossum = np.sum(np.arange(w)[ind])
    maskposnum = np.sum(np.ones(w)[ind])
    maskposf = maskpossum/maskposnum
    # print("maskpos "+str(maskposf))
    masksum=319-(masksum/masksum.max())*100
    maskview=319-(maskview/maskview.max())*100
    # Draw overlay graphs
    pts = np.vstack((np.arange(w),masksum)).astype(np.int32).T
    ptsx = np.vstack((np.arange(w),maskview)).astype(np.int32).T  
    pts2 = np.vstack((np.arange(240),shades[0:240])).astype(np.int32).T
    cv2.polylines(mmatch, [ptsx], isClosed=False, color=(255,0,0))
    cv2.polylines(frame,  [pts], isClosed=False, color=(255,0,0))
    cv2.polylines(frame,  [pts2], isClosed=False, color=(0,256,0))
    cv2.polylines(mmatch, [pts2], isClosed=False, color=(0,256,0))
    pts5 = np.vstack((np.array([blackThreshold,blackThreshold]),np.array([1,100]))).astype(np.int32).T
    cv2.polylines(mmatch, [pts5], isClosed=False, color=(255,0,0))

    pts4 = np.vstack((np.array([w/2,w/2]),np.array([200,300]))).astype(np.int32).T
    cv2.polylines(frame, [pts4], isClosed=True, color=(0,256,0))

    if maskposnum != 0:
        maskpos=int(maskposf)
        pts3 = np.vstack((np.array([maskpos,maskpos]),np.array([200,300]))).astype(np.int32).T
        # cv2.polylines(mmatch, [pts3], isClosed=True, color=(0,256,0))
        cv2.polylines(frame, [pts3], isClosed=True, color=(256,256,0))

    # Try other thresholding
    img = cv2.GaussianBlur(img2gray,(13,13),0)
    maskam = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,11,2)
    maskag = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    ret, masko = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    out.write(frame)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('adaptive mean',maskam)
    cv2.imshow('adaptive gaussian',maskag)
    cv2.imshow('otsu thresholding',masko)
    cv2.imshow('histo',mmatch)

    keyOut = cv2.waitKey(25) & 0xFF
    if keyOut == ord('q'):
        break
    if keyOut == ord('p'):
        # Wait p unpress
        while keyOut == ord('p'):
            keyOut = cv2.waitKey(25) & 0xFF
        while keyOut != ord('p'):
            keyOut = cv2.waitKey(25) & 0xFF


cap.release()
out.release()
cv2.destroyAllWindows()