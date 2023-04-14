using System;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Net;

namespace McSkillTest
{
    class Program
    {

        static void Main(string[] args)
        {
            string jdkUrl = "https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jdk/jdk-8u361-windows-x64.zip";
            string jarUrl = "https://mcskill.net/McSkillTest.jar";

            string tempFolder = Path.Combine(Path.GetTempPath(), "McSkillTest");

            Directory.CreateDirectory(tempFolder);

            string jdkFileName = Path.Combine(tempFolder, "jdk.zip");
            string jdkFolder = Path.Combine(tempFolder, "jdk");
            string jarFileName = Path.Combine(tempFolder, "McSkillTest.jar");

            bool jdkExists = Directory.Exists(jdkFolder);
            bool jarExists = File.Exists(jarFileName);

            if (!jdkExists)
            {
                static async Task DownloadJDKAsync(string jdkUrl, string jdkFileName)
                {
                    using (var client = new WebClient())
                    {
                        Console.WriteLine($"Загрузка JDK...");

                        int previousPercentage = 0;

                        client.DownloadProgressChanged += (sender, e) =>
                        {
                            int percentage = e.ProgressPercentage;

                            if (percentage != previousPercentage)
                            {
                                Console.Write($"\r[ {percentage}% ]");
                                previousPercentage = percentage;
                            }
                        };

                        await client.DownloadFileTaskAsync(jdkUrl, jdkFileName);

                        Console.WriteLine("\rЗагрузка завершена.");
                    }
                }

                DownloadJDKAsync(jdkUrl, jdkFileName).Wait();

                Console.WriteLine($"Распаковка JDK...");
                ZipFile.ExtractToDirectory(jdkFileName, jdkFolder);

                Console.WriteLine("Очистка мусора...\n");
                File.Delete(jdkFileName);
            }

            if (!jarExists)
            {
                using (var client = new WebClient())
                {
                    Console.WriteLine($"Загрузка лаунчера...");
                    client.DownloadFile(jarUrl, jarFileName);
                }
                Console.WriteLine("Загрузка завершена.");
            }

            string javaExe = Path.Combine(jdkFolder, "jdk1.8.0_361", "bin", "java.exe");
            string jarArgs = $"-jar \"{jarFileName}\"";
            Console.WriteLine($"Запуск лаунчера");

            var process = new Process();
            process.StartInfo.FileName = javaExe;
            process.StartInfo.Arguments = jarArgs;
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardError = true;
            process.StartInfo.CreateNoWindow = true;

            process.EnableRaisingEvents = true;
            Console.CancelKeyPress += (sender, e) =>
            {
                e.Cancel = true;
                process.Kill();
            };

            process.Start();
        }
    }
}