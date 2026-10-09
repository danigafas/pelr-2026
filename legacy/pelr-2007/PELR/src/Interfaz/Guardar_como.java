/*
 * Guardar_como.java
 *
 * Created on 20 de abril de 2007, 10:51
 */

package Interfaz;

import javax.swing.*;
import java.io.*;
import java.util.*;
        
class Guardar_como extends JPanel
{
   String filename;

   /**
    *@param n Nombre del fichero a tratar
    *@return Devuelve el nombre del fichero, añadiendo al final .txt si es que no lo tenia ya.
    */
   public String tratarNombreFichero(String n)
      {
        String extension=".txt";
        if (n.charAt(n.length()-4) != '.')
            n=n+extension;
        return n;
      }


  Guardar_como()
  {}


  Guardar_como (JPanel panel_ppal)
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
           if (fich.showSaveDialog(panel_ppal)==JFileChooser.APPROVE_OPTION) {
               filename=tratarNombreFichero(fich.getSelectedFile().getAbsolutePath());
           }
           else filename="";

  }
}

