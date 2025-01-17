# <h1>Python implementation for Grab Demo</h1>
# <h2>How to Run:&nbsp;</h2>
# <p>Follow the steps within the <a href="sapera_test.py">Python Implementation
#         file</a> for the Sapera LT.&nbsp; Ensure that you have run the C# Grab
#     Demo at least once to generate the DLL file needed for this. Check to make
#     sure that your files are located within the same directories that are used
#     within this script. If not, change them accordingly. Once everything is
#     installed, activate your Python environment, and run this script.</p>
# <h2>Current Implementation:</h2>
# <p>The code within this file contains an attempt at initializing the needed
#     classes to perform the functions from the Sapera SDK. This file is
#     intended to mimic how the grab demo initializes the components. The
#     variable names and function names are the same in this file and within the
#     grab demo.&nbsp;</p>
import sys
import clr

# <p>To use this file, you must build the Sapera GrabDemo once</p>
sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Demos/NET/GrabDemo/CSharp/bin/Debug")

clr.AddReference("SapNETCSharpGrabDemo")

from DALSA.SaperaLT.Demos.NET.CSharp.GrabDemo import *
from DALSA.SaperaLT.SapClassGui import *

# <p>Calling the GramDemoDlg directly like this causes a portion of the existing
#     C# grab demo GUI to appear to start a connection when a server is found.
#     This was discovered during our testing on Dr. Leondard's equipment &amp;
#     calling this function directly will not work for the new GUI.</p>
#grabDemo = GrabDemoDlg()

# <p>Attempt to call on click button function. This does end in an error, but it
#     proves that the function can be found &amp; called. To run without error
#     it just needs the correct arguments provided.</p>
#grabDemo.button_New_Click()

# <p>Add the Sapera .dlls to the Path</p>
sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Components/NET/Bin")

# <p>We can reference the SapClassBasic and the Windows built-in forms to access
#     everything we should need.</p>
clr.AddReference("DALSA.SaperaLT.SapClassBasic")
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import *
from DALSA.SaperaLT.SapClassBasic import *

# <p>This is the start of the <a
#         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemoDlg.cs#GrabDemoDlg">GrabDemoDlg()</a>
#     function within the grab demo. This function is originally called from
#     Main() in <a
#         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemo.cs">GrabDemo.cs</a>
# </p>

# <p>Here, we instantiate the .NET variables to use to define the acquisition
# </p>
m_Acquisition = SapAcquisition()
m_Buffers = SapBuffer()
m_Xfer = SapAcqToBuf(m_Acquisition, m_Buffers)
m_View = SapView()
m_IsSignalDetected = True
m_ServerLocation = SapLocation()

# <p>AcqConfigDlg() is a function within the grab demo. It needs to be
#     determined if this function is fine as is called directly from the grab
#     functions dll, needs to be ported over to python, or for the values to be
#     hard coded. This function does cause part of the preexisting C# grab
#     demo's GUI to appear and will allow you to make a connection if a server
#     is found within this GUI. It will work in this case as these values
#     returned to acConfigDlg can be used for the rest of the SDK's functions
#     called this Python script to create the needed objects.&nbsp;</p>
# <p><span style="background-color: rgb(251, 238, 184);">As of 2023-04-07, we
#         discussed with Dr. Leonard and he said that he would like to stay away
#         from having the old C# grab demo's GUI pop up for this. This would
#         mean that the AcqConfigDlg() needs to be looked into porting into
#         Python if possible.&nbsp;</span></p>
# <p>Dr. Leonard provided us with the <a href="jAi_SW-4000M_1x10.ccf"
#         target="_blank" rel="noopener">config file</a> (this link will just
#     download the config file on your desktop, but it is located here:
#     StandardMechanics\Image-acquisition-GUI\Python\jAi_SW-4000M_1x10.ccf) that
#     he uses. He said that it is the only config file that he uses so he does
#     not mind if this file is hard-coded in to be automatically used. As
#     discussed with Dr. Leonard, I believe this config file should also be
#     updated on any changes to the camera settings that are being done within
#     the&nbsp;<a href="../../Serial-Communications/README.cchtml">other
#         project</a>. This will need to be discussed with the other team
#     working on that project.&nbsp;</p>
# <p>This acConfigDlg reads config settings, shows the dialogue window</p>
acConfigDlg = AcqConfigDlg(None, "", AcqConfigDlg.ServerCategory.ServerAcq)
dialog_result = acConfigDlg.ShowDialog()
print(dialog_result)
# <p>Set m_online based on if the Dialog populated correctly. This should work
#     if the Sapera server exists</p>
if (dialog_result == DialogResult.OK):
    m_online = True
else:
    m_online = False
print(m_online)

num_servers = SapManager.GetServerCount(SapManager.ResourceType.Acq)
print(num_servers)


# <p>GrabDemoDlg() calls a function named <a
#         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemoDlg.cs#CreateNewObjects1">CreateNewObjects()</a>.
#     This is the implementation of that function. There are errors within this
#     function due to trying to tryinig to use the create() function for
#     SapAcquisition() with no server. SapTransfer.Create() will also fail due
#     to SapAcquisition not creating successfully. SapAcquisition.Create() has
#     to be ran first and be successful for SapTransfer.Create() to succeed.</p>
def CreateNewObjects(acConfigDlg, Restore):
    global m_Acquisition
    global m_Buffers
    global m_Xfer
    global m_View
    global m_ServerLocation
    
    if (m_online):
        if (not Restore):
            m_ServerLocation = acConfigDlg.ServerLocation
            m_ConfigFileName = acConfigDlg.ConfigFile
        
        m_Acquisition = SapAcquisition(m_ServerLocation, m_ConfigFileName)
        print(m_ServerLocation)
        print(m_ConfigFileName)

        if (SapBuffer.IsBufferTypeSupported(m_ServerLocation, SapBuffer.MemoryType.ScatterGather)):
            m_Buffers = SapBufferWithTrash(2, m_Acquisition, SapBuffer.MemoryType.ScatterGather)
            print(1)
        else:
            m_Buffers = SapBufferWithTrash(2, m_Acquisition, SapBuffer.MemoryType.ScatterGatherPhysical)
            print(2)
        m_Xfer = SapAcqToBuf(m_Acquisition, m_Buffers)
        m_View = SapView(m_Buffers)
        print(m_Buffers.TrashType)
        print(m_Xfer)
        print(m_View)

        m_Xfer.Pairs[0].EventType = SapXferPair.XferEventType.EndOfFrame
        
        # <p>These Notify functions need to be looked further into to determine
        #     what needs to be added here.</p>
        #m_Xfer.XferNotify += SapXferNotifyHandler(grabDemo.xfer_XferNotify)
        #m_Xfer.XferNotifyContext = grabDemo
        

        #m_Acquisition.SignalNotify += SapSignalNotifyHandler(grabDemo.GetSignalStatus)
        #m_Acquisition.SignalNotifyContext = grabDemo
    else:
        m_Buffers = SapBuffer()
        m_View = SapView(m_Buffers)

    # <p>Within the first CreateNewObjects() function it calls a <a
    #         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemoDlg.cs#CreateNewObjects2">CreateObjects()</a>
    #     function. There are a couple of CreateNewObjects() functions within
    #     the grab demo due to function overloading. This is the start of the
    #     next function and where the errors occur.</p>
    # <p>This section may need to be split into a separate function similar to
    #     how it is within the grab demo to handle failure returns and so
    #     DisposeObjects() can be called at the proper time on failure.&nbsp;
    # </p>
    if (m_Acquisition != None and not m_Acquisition.Initialized):
        if (m_Acquisition.Create() == False):
            # <p><span style="background-color: rgb(248, 202, 198);">NOT
            #         TESTED</span>, but I went back to see when
            #     DestoryObjects() was called after meeting with Dr. Leonard
            #     &amp; it needs to be called here if create fails and in
            #     several other locations. Also needs to be called if any of the
            #     following creates fail as well.</p>
            print("m_Acquisition create failed")
        else:
            print("m_Acquisition create success")
    
    if (m_Buffers != None and not m_Buffers.Initialized):
        if (m_Buffers.Create() == False):
            #DestoryObjects()
            print("m_Buffers create failed")
        else:
            print("m_Buffers create success")
    
    if (m_View != None and not m_View.Initialized):
        if (m_View.Create() == False):
            #DestoryObjects()
            print("m_View create failed")
        else:
            print("m_View create success")
    
    if (m_Xfer != None and not m_Xfer.Initialized):
        if (m_Xfer.Create() == False):
            #DestoryObjects()
            print("m_Xfer create failed")
            DestoryObjects()
        else:
            print("m_Xfer create success")
    
    # <p>Attempt to use the Grab function from SapTransfer(). This should be
    #     successful if m_Xfer can create successfully. It needs a server
    #     connection to create successfully so currently this function is
    #     failing also due to the unsuccessful create. As seen within the grab
    #     demo, this function Grab() can be used for the grab button. There are
    #     also functions under SapTransfer for Freeze and Snap that can be used
    #     for those buttons similar to how the grab demo is using them.</p>
    # <p><span style="background-color: rgb(248, 202, 198);">TODO</span>: The
    #     function call to Grab() is just here for testing purposes currently
    #     &amp; will need to be removed for final implementation. This is just
    #     proof that the function can be called &amp; works when the connection
    #     is successful.&nbsp;</p>
    m_Xfer.Grab()
CreateNewObjects(acConfigDlg, False)

# <p>This function,<a
#         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemoDlg.cs#EnableSignalStatus">
#         EnableSignalStatus()</a>, is called from the first CreateNewObjects()
#     function within the grab demo.</p>
def EnableSignalStatus():
    if (m_Acquisition != None):
        print(m_Acquisition.SignalStatus)
        print(SapAcquisition.AcqSignalStatus(0))
        m_IsSignalDetected = (m_Acquisition.SignalStatus != (SapAcquisition.AcqSignalStatus(0)))
        if (not m_IsSignalDetected):
            print("Online... No camera signal detected")
        else:
            print("Online... camera signal detected")
        m_Acquisition.SignalNotifyEnable = True

EnableSignalStatus()

# <p>This function, <a
#         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemoDlg.cs#DestroyObjects">DestroyObjects()</a>,
#     closes all connections and can be found within the grab demo. It is used
#     in several different locations within the grab demo to end all
#     connections. This was added in during our testing on Dr. Leonard's
#     equipment. Without this function called at the end of the script/ closing
#     of the GUI / anytime the connections need to be changed, the connections
#     will remain &amp; the script will fail to run again due to the connections
#     being in use already.&nbsp;</p>
def DestroyObjects():
    if (m_Xfer != None and m_Xfer.Initialized):
        m_Xfer.Destroy()
    if (m_View != None and m_View.Initialized):
        m_View.Destroy()
    if (m_Buffers != None and m_Buffers.Initialized):
        m_Buffers.Destroy()
    if (m_Acquisition != None and m_Acquisition.Initialized):
        m_Acquisition.Destroy()
DestroyObjects()

# <p>I would assume <a
#         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemoDlg.cs#DisposeObjects">DisposeObjects()</a>,
#     not yet implemented in this script <span
#         style="background-color: rgb(248, 202, 198);">(TODO)</span>, is
#     similar to DestroyObjects(). DisposeObjects() is supposed to be called
#     when any of the objects fail to create and in the same locations where the
#     connections are closed with DestroyObjects().&nbsp;</p>
# <h2>Notes:</h2>
# <p><span style="background-color: rgb(251, 238, 184);">As of 2023-04-07, we've
#         run the above code on Dr. Leonard's hardware, and confirmed that it
#         all works correctly, and is ready for the next team to continue work
#         with. The connections were all created successfully, the server was
#         found, and the camera signal was detected during this
#         testing.&nbsp;</span></p>

# <p>Most buttons in the dialogue operate based on m_Xfer to determine how/when
#     to use them.</p>
# <p>The Line-scan/Area-scan buttons instead operate directly off of
#     m_Acquisition, and are only populated in the C++ version of the library.
# </p>
# <p>It would be possible to instantiate these buttons too, except that the
#     dialogues they would need to populate do not exist in the common C#
#     library of the demos.</p>
# <p>Creating the Linescan option seems to require writing a C# dialogue for
#     that</p>
# <p>&nbsp;</p>
# <h2><strong>Next Steps:</strong>&nbsp;</h2>
# <ul>
#     <li>Look into porting AcqConfigDlg() into Python with the config file
#         provided by Dr. Leonard automatically used.</li>
#     <li>Reformat code to be able to be used by new GUI</li>
#     <li>Follow along the path in GrabDemoDlg.cs that is called from main()
#         from GrabDemo.cs as previously described. Currently, this Python
#         script goes through most of it, but there may be missing sections
#         &amp; needs to be double-checked to ensure proper functionality. Some
#         of the functions need to be moved around &amp; called from different
#         locations such as the EnableSignalStatus() function should be called
#         from within the CreateNewObjects() function, but is currently just
#         called from the main section.&nbsp;</li>
#     <li>Implement error handling for failures. This should just be simple
#         calls to DestoryObjects() and DisposeObjects() mostly. The
#         CreateNewObjects() function should return a boolean value depending on
#         if the connections are made successfully. Same for CreateObjects(), it
#         returns a boolean depending on success/failure. Currently, there are a
#         lot of errors if you are testing with no hardware.&nbsp;</li>
#     <li>Split the CreateObjects() function out of CreateNewObjects() function
#         within this script so that it can properly handle failures and know
#         when to call DisposeObjects(). This will follow how it is currently
#         already implemented within the C# grab demo so you should be able to
#         just follow how it is implemented there.&nbsp;</li>
#     <li>Implement functions for button presses, and ensure that these can be
#         directly called from the new GUI.</li>
#     <li>Look further into how to implement the select/deselect trigger
#         function within the Line Scan Modal. As Dr. Leonard said, this is the
#         only function he uses within this modal. This function is not within
#         the C# Grab demo implementation and can be found within the C++
#         implementation of the Grab Demo.&nbsp;</li>
# </ul>
