using UnityEngine;
using Python.Runtime;
using System.Threading.Tasks;

public class PythonRunner : MonoBehaviour
{
    public Animator animator;
    public string movementStyle = "idle";

    public void PredictAI(bool ran, bool hid, bool used_forest, float distance_to_player)
    {
        Task.Run(() =>
        {
            Debug.Log("Initializing Python...");
            Runtime.PythonDLL = Application.dataPath + "/Plugins/Python/python310.dll";
            PythonEngine.Initialize();
            Debug.Log("Python initialized");

            using (Py.GIL())
            {
                try
                {
                    PythonEngine.Exec("import sys");
                    PythonEngine.Exec(@"sys.path.append(r'" + Application.dataPath.Replace(@"\", @"\\") + @"\\PythonScripts')");

                    dynamic brain = Py.Import("AiBrain");

                    dynamic result = brain.predict_attack(ran, hid, used_forest, distance_to_player);
                    string predictedAttack = result[0].ToString();
                    string predictedMoveStyle = result[1].ToString();

                    Debug.Log("Predicted attack: " + predictedAttack);
                    Debug.Log("Predicted movement style: " + predictedMoveStyle);

                    movementStyle = predictedMoveStyle;

                    UnityMainThreadDispatcher.Instance().Enqueue(() =>
                    {
                        if (animator != null)
                        {
                            animator.SetTrigger(predictedAttack);
                            animator.SetBool("charge", false);
                            animator.SetBool("stealth", false);
                            animator.SetBool("limp", false);
                            animator.SetBool(predictedMoveStyle, true);
                        }
                    });
                }
                catch (System.Exception ex)
                {
                    Debug.LogError("Python error: " + ex);
                }
            }

            PythonEngine.Shutdown();
            Debug.Log("Python engine shut down");
        });
    }
}
