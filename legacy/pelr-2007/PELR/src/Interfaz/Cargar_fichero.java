/*
 * Cargar_fichero.java
 *
 * Created on 20 de abril de 2007, 13:07
 */

package Interfaz;

import javax.swing.*;
import java.io.*;
import java.util.*;
        
class Cargar_fichero extends JPanel
{
    String filename;

    Cargar_fichero()
    {}


    Cargar_fichero (JPanel panel_ppal)
    {
        JFileChooser fich=new JFileChooser();

        fich.setFileFilter(new javax.swing.filechooser.FileFilter()
        {
            public boolean accept(File file)
            {
                String filename=file.getName();
                if (file.isDirectory()) return true;
                return (filename.endsWith(".txt"));
            }

            public String getDescription()
             {
               return "Ficheros txt (*.txt)";
             }
           } );
     
           fich.setSize(400,300);
           fich.setCurrentDirectory(new File("."));
           if (fich.showOpenDialog(panel_ppal)==JFileChooser.APPROVE_OPTION) {
               filename=fich.getSelectedFile().getAbsolutePath();
           }
           else filename="";

  }
    
}
