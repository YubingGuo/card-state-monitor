import os
import re
import subprocess
import signal
import logging

from timeout import Timeout
#import eatt_helper

class CmdExecutor(object):

    def __init__(self, timeout):
        self._timeout = timeout

    def execute_command(self, cmd):
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=True)
        return self._wait_for_execution_result(proc)

    def _wait_for_execution_result(self, proc):
        timeout = Timeout(self._timeout)
        try:
            while timeout.is_not_reached():
                if self._is_process_working(proc):
                    continue
                return self._read_process_data(proc)
            proc.send_signal(signal.SIGINT)
            proc.send_signal(signal.SIGQUIT)
        except:
            raise TimeoutException()

    def _is_process_working(self, proc):
        rc = proc.poll()
        return True if rc is None else False

    def _read_process_data(self, proc):
        stdout, stderr = proc.communicate()
        rc = proc.poll()
        return stdout, stderr, rc

class EattHelper():
    def __init__(self, eatt_root_path):
        self.eatt_root_path = eatt_root_path
        self.att_bin_path = os.path.join(self.eatt_root_path, r'ATT_Engine_Tcl85\NewATTEngineReleasePacket\bin')
        #self.cmdExecutor = CmdExecutor(10)
        
    def Execute(self, att_command, timeout = 5):
        os.chdir(self.att_bin_path)
        
        cmdExecutor = CmdExecutor(timeout)
        try:
            stdout, stderr, rc = cmdExecutor.execute_command(att_command)
        except:
            logging.error('Connect to eNB failed!')
            return (False, 'Connect to eNB failed!')

        connect_failure = re.findall( r'.*(Failed[\x20]?to[\x20]?connect[\x20]?to.*|Failed[\x20]?to[\x20]?FTP[\x20]?download.*)', stdout, re.I|re.M)
        if len(connect_failure):
            logging.error(str(connect_failure))
            return (False, str(connect_failure))
        else:
            #execute_failure = re.findall(r'^VERDICT_COMMENT : FAIL.*', result. re.I|re.M)
            #if len(execute_failure):
            if r'VERDICT_COMMENT : FAIL' in stdout:
                logging.error('Execute command failed!')
                logging.error('=====ERROR=====')
                logging.error(stdout)
                logging.error('================')
                return (False, 'Execute command failed!')

        logging.info('Execute command successfully!')
        return (True, None)
        
    def CardControl(self, slot_id, ctrl_id):
        att_command = ' '.join(('ATT.exe', 'cardControl.tcl', str(slot_id), str(ctrl_id)))
        return self.Execute(att_command)

    def CardCheck(self, slot_id):
        pass

