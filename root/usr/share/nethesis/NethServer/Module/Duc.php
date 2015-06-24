<?php
namespace NethServer\Module;
/*
 * Copyright (C) 2013 Nethesis S.r.l.
 * http://www.nethesis.it - support@nethesis.it
 *
 * This script is part of NethServer.
 *
 * NethServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * NethServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with NethServer.  If not, see <http://www.gnu.org/licenses/>.
 */

class Duc extends \Nethgui\Controller\AbstractController
{
    const DUC_PATH='/var/cache/duc/duc.json';

    public $sortId = 40;

    protected function initializeAttributes(\Nethgui\Module\ModuleAttributesInterface $attributes)
    {
        $a = \Nethgui\Module\SimpleModuleAttributesProvider::extendModuleAttributes($attributes, 'Status');
        return new \NethServer\Tool\CustomModuleAttributesProvider($a, array('languageCatalog' => array('NethServer_Module_Duc', 'NethServer_Module_Dashboard_Duc')));
    }

    public function prepareView(\Nethgui\View\ViewInterface $view) {
        if($this->getRequest()->hasParameter('get_json')) {
           header('Content-type: application/json; charset: utf-8');
           echo $this->getPhpWrapper()->file_get_contents(self::DUC_PATH);
           exit();
        }
        parent::prepareView($view);
         // get stat info of duc.json file
        $stat = $this->getPhpWrapper()->stat('/var/cache/duc/duc.json');
        if($stat) {
             $timestamp = $stat['mtime'];
             $date = $this->getPhpWrapper()->gmdate($view->translate('Date_Format'), $timestamp);
        } else {
             $date = $view->translate('Not_Updated_Duc_Label');
        }
        $view['date'] = $date;
    }

    public function process()
    {
        parent::process();

        if ($this->getRequest()->isMutation()) {
            // Signal nethserver-duc-save event
            $this->getPlatform()->signalEvent('nethserver-duc-save &');
        }
    }
}
